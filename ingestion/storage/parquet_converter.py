"""
NexusGov - Conversor de Dados para Parquet Particionado (RF-ING-04)
Organiza os datasets analíticos por competência e UF.
"""

from pathlib import Path
from typing import List, Optional
import pyarrow as pa
import pyarrow.parquet as pq
from ..models.payloads import PncpContratacao

class ParquetStorageConverter:
    """Converte listas de contratações e itens em tabelas Parquet particionadas."""

    def __init__(self, output_dir: Optional[Path] = None):
        root = Path(__file__).resolve().parent.parent.parent
        self.output_dir = output_dir or (root / "data" / "processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_contratacoes_parquet(
        self,
        contratacoes: List[PncpContratacao],
        competencia: str,
        uf: str = "PB"
    ) -> Path:
        """Salva a lista de contratações em Parquet com particionamento por competência e UF."""
        dest_dir = self.output_dir / f"competencia={competencia}" / f"uf={uf.upper()}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / "contratacoes.parquet"

        records = []
        for c in contratacoes:
            records.append({
                "numero_controle_pncp": c.numero_controle_pncp,
                "orgao_cnpj": c.orgao_cnpj,
                "orgao_nome": c.orgao_nome,
                "esfera": c.esfera,
                "poder": c.poder,
                "uf": c.uf,
                "codigo_ibge_municipio": c.codigo_ibge_municipio,
                "modalidade_nome": c.modalidade_nome,
                "numero_edital": c.numero_edital,
                "ano_compra": c.ano_compra,
                "objeto": c.objeto,
                "valor_total_estimado": c.valor_total_estimado,
                "valor_total_homologado": c.valor_total_homologado,
                "data_abertura_proposta": c.data_abertura_proposta.isoformat() if c.data_abertura_proposta else None,
                "data_homologacao": c.data_homologacao.isoformat() if c.data_homologacao else None,
                "situacao": c.situacao,
                "url_pncp": c.url_pncp,
                "qtd_itens": len(c.itens)
            })

        table = pa.Table.from_pylist(records)
        pq.write_table(table, dest_file, compression="SNAPPY")
        return dest_file
