"""
NexusGov - Testes de Parser da Receita Federal (RF-ING-03, RF-ING-04, RF-ING-05)
"""

from pathlib import Path
import duckdb
import pytest
from ingestion.parsers.receita import ReceitaFederalParser

def test_parse_estabelecimentos_filtering_pb(tmp_path: Path):
    parser = ReceitaFederalParser(output_dir=tmp_path)

    # Cria CSV de teste simulando o dump da Receita Federal (com colunas separadas por ponto e vírgula)
    # Linha 1: Empresa na PB (João Pessoa)
    # Linha 2: Empresa em SP (deve ser filtrada)
    # Linha 3: Empresa na PB (Campina Grande)
    csv_file = tmp_path / "estabelecimentos_test.csv"
    lines = [
        # c0..c13, c14(logr), c15(num), c16(compl), c17(bairro), c18(cep), c19(uf), c20(municipio), c21(ddd1), c22(tel1)...
        '"12345678";"0001";"95";"1";"NEXUS PB";"02";"20200101";"00";"";"";"20200101";"6201500";"";"RUA";"EPITACIO PESSOA";"100";"";"CENTRO";"58000000";"PB";"2507507";"83";"32110000";"";"";"";"";"contato@nexus.pb";"";""',
        '"99999999";"0001";"11";"1";"OUTRO SP";"02";"20200101";"00";"";"";"20200101";"6201500";"";"AV";"PAULISTA";"1000";"";"BELA VISTA";"01310000";"SP";"3550308";"11";"31000000";"";"";"";"";"contato@sp.com";"";""',
        '"87654321";"0001";"44";"1";"CAMPINA TECH";"02";"20210510";"00";"";"";"20210510";"6202300";"";"RUA";"FLORIANO PEIXOTO";"500";"";"CENTRO";"58400000";"PB";"2504009";"83";"33100000";"";"";"";"";"tech@campina.pb";"";""'
    ]
    csv_file.write_text("\n".join(lines), encoding="utf-8")

    parquet_result = parser.parse_estabelecimentos(
        csv_path=csv_file,
        competencia="2026-09",
        target_uf="PB"
    )

    assert parquet_result.exists()

    # Valida via DuckDB que apenas os 2 registros da Paraíba (PB) foram mantidos
    con = duckdb.connect(database=":memory:")
    df = con.execute(f"SELECT * FROM read_parquet('{parquet_result.as_posix()}')").fetchall()
    assert len(df) == 2

    # Verifica os CNPJs completos
    cnpjs = {r[0] for r in df}
    assert "12345678000195" in cnpjs
    assert "87654321000144" in cnpjs
    assert "99999999000111" not in cnpjs # O de SP foi excluído
