"""
NexusGov - Parser dos Dumps da Receita Federal (RF-ING-03, RF-ING-04, RF-ING-05)
Processamento colunar em blocos (chunks) com DuckDB e particionamento por competência e UF (PB).
"""

from pathlib import Path
from typing import Dict, List, Optional, Set
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
from .schema_validator import SchemaValidator

class ReceitaFederalParser:
    """
    Parser streaming de arquivos de CNPJ da Receita Federal com DuckDB.
    Filtra estabelecimentos domiciliados na Paraíba (PB) e converte para Parquet.
    """

    def __init__(self, output_dir: Optional[Path] = None):
        root = Path(__file__).resolve().parent.parent.parent
        self.output_dir = output_dir or (root / "data" / "processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(database=":memory:")

    def parse_estabelecimentos(
        self,
        csv_path: Path,
        competencia: str,
        target_uf: str = "PB",
        supplier_cnpjs: Optional[Set[str]] = None
    ) -> Path:
        """
        Processa dump de Estabelecimentos filtrando por UF (PB) e fornecedores cadastrados.
        Gera Parquet particionado: data/processed/competencia=YYYY-MM/uf=PB/estabelecimentos.parquet
        """
        dest_dir = self.output_dir / f"competencia={competencia}" / f"uf={target_uf.upper()}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / "estabelecimentos.parquet"

        # Define colunas padrão da Receita Federal
        cols = SchemaValidator.RECEITA_ESTABELECIMENTOS_COLUMNS
        col_names = ", ".join([f"column{i:02d} AS {name}" for i, name in enumerate(cols)])

        query = f"""
        CREATE OR REPLACE TABLE raw_estabelecimentos AS
        SELECT {col_names}
        FROM read_csv(
            '{csv_path.as_posix()}',
            header=false,
            delim=';',
            quote='"',
            escape='"',
            all_varchar=true,
            ignore_errors=true
        )
        WHERE upper(trim(column19)) = '{target_uf.upper()}'
        """

        self.con.execute(query)

        # Se houver filtro de CNPJs do PNCP (RF-ING-05), aplica junção/filtro
        if supplier_cnpjs:
            cnpjs_tuple = "('" + "', '".join(supplier_cnpjs) + "')"
            filter_sql = f"AND (cnpj_basico || cnpj_ordem || cnpj_dv) IN {cnpjs_tuple}"
        else:
            filter_sql = ""

        export_query = f"""
        COPY (
            SELECT 
                (cnpj_basico || cnpj_ordem || cnpj_dv) AS cnpj_completo,
                cnpj_basico,
                nome_fantasia,
                situacao_cadastral,
                data_inicio_atividade,
                cnae_fiscal_principal,
                tipo_logradouro,
                logradouro,
                numero,
                complemento,
                bairro,
                cep,
                uf,
                municipio,
                (ddd_1 || telefone_1) AS telefone_principal,
                correio_eletronico AS email
            FROM raw_estabelecimentos
            WHERE 1=1 {filter_sql}
        ) TO '{dest_file.as_posix()}' (FORMAT PARQUET, COMPRESSION SNAPPY)
        """

        self.con.execute(export_query)
        return dest_file

    def parse_socios(
        self,
        csv_path: Path,
        competencia: str,
        relevant_cnpj_basics: Optional[Set[str]] = None,
        target_uf: str = "PB"
    ) -> Path:
        """
        Processa dump do Quadro de Sócios e Administradores (QSA).
        Gera Parquet particionado: data/processed/competencia=YYYY-MM/uf=PB/socios.parquet
        """
        dest_dir = self.output_dir / f"competencia={competencia}" / f"uf={target_uf.upper()}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / "socios.parquet"

        cols = SchemaValidator.RECEITA_SOCIOS_COLUMNS
        col_names = ", ".join([f"column{i:02d} AS {name}" for i, name in enumerate(cols)])

        query = f"""
        CREATE OR REPLACE TABLE raw_socios AS
        SELECT {col_names}
        FROM read_csv(
            '{csv_path.as_posix()}',
            header=false,
            delim=';',
            quote='"',
            escape='"',
            all_varchar=true,
            ignore_errors=true
        )
        """
        self.con.execute(query)

        filter_sql = ""
        if relevant_cnpj_basics:
            basics_tuple = "('" + "', '".join(relevant_cnpj_basics) + "')"
            filter_sql = f"WHERE cnpj_basico IN {basics_tuple}"

        export_query = f"""
        COPY (
            SELECT 
                cnpj_basico,
                identificador_socio,
                nome_socio,
                cnpj_cpf_socio AS cpf_mascarado,
                qualificacao_socio,
                data_entrada_sociedade,
                faixa_etaria
            FROM raw_socios
            {filter_sql}
        ) TO '{dest_file.as_posix()}' (FORMAT PARQUET, COMPRESSION SNAPPY)
        """

        self.con.execute(export_query)
        return dest_file
