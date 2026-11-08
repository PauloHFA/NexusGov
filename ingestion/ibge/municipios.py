"""
NexusGov - Importador e Base de Municípios do IBGE (RF-ING-07)
Especialização para o Escopo Piloto da Paraíba (UF: PB, código IBGE 25)
"""

import math
from typing import Dict, List, Optional
from pydantic import BaseModel

class MunicipioIBGE(BaseModel):
    codigo_ibge: str
    nome: str
    uf: str
    latitude: float
    longitude: float

# Coletânea de referência dos principais municípios e microrregiões da Paraíba (PB - 25)
MUNICIPIOS_PARAIBA_REFERENCIA = [
    MunicipioIBGE(codigo_ibge="2507507", nome="João Pessoa", uf="PB", latitude=-7.11532, longitude=-34.8631),
    MunicipioIBGE(codigo_ibge="2504009", nome="Campina Grande", uf="PB", latitude=-7.23056, longitude=-35.8811),
    MunicipioIBGE(codigo_ibge="2513703", nome="Santa Rita", uf="PB", latitude=-7.11389, longitude=-34.9781),
    MunicipioIBGE(codigo_ibge="2510808", nome="Patos", uf="PB", latitude=-7.02583, longitude=-37.2800),
    MunicipioIBGE(codigo_ibge="2501500", nome="Bayeux", uf="PB", latitude=-7.12500, longitude=-34.9322),
    MunicipioIBGE(codigo_ibge="2516201", nome="Sousa", uf="PB", latitude=-6.76111, longitude=-38.2278),
    MunicipioIBGE(codigo_ibge="2503209", nome="Cabedelo", uf="PB", latitude=-6.98111, longitude=-34.8339),
    MunicipioIBGE(codigo_ibge="2503704", nome="Cajazeiras", uf="PB", latitude=-6.88889, longitude=-38.5583),
    MunicipioIBGE(codigo_ibge="2506301", nome="Guarabira", uf="PB", latitude=-6.85500, longitude=-35.4900),
    MunicipioIBGE(codigo_ibge="2509107", nome="Mamanguape", uf="PB", latitude=-6.83889, longitude=-35.1250),
    MunicipioIBGE(codigo_ibge="2512507", nome="Queimadas", uf="PB", latitude=-7.35972, longitude=-35.8989),
    MunicipioIBGE(codigo_ibge="2513901", nome="São Bento", uf="PB", latitude=-6.48889, longitude=-37.4528),
    MunicipioIBGE(codigo_ibge="2509701", nome="Monteiro", uf="PB", latitude=-7.88944, longitude=-37.1250),
    MunicipioIBGE(codigo_ibge="2506004", nome="Esperança", uf="PB", latitude=-7.02389, longitude=-35.8569),
    MunicipioIBGE(codigo_ibge="2512101", nome="Pombal", uf="PB", latitude=-6.77194, longitude=-37.7989),
    MunicipioIBGE(codigo_ibge="2504306", nome="Catolé do Rocha", uf="PB", latitude=-6.34389, longitude=-37.7478),
    MunicipioIBGE(codigo_ibge="2506905", nome="Itabaiana", uf="PB", latitude=-7.32972, longitude=-35.3331),
    MunicipioIBGE(codigo_ibge="2512309", nome="Princesa Isabel", uf="PB", latitude=-7.73694, longitude=-37.9939),
    MunicipioIBGE(codigo_ibge="2500601", nome="Alagoa Grande", uf="PB", latitude=-7.04500, longitude=-35.6269),
    MunicipioIBGE(codigo_ibge="2515906", nome="Solânea", uf="PB", latitude=-6.72194, longitude=-35.6939),
    MunicipioIBGE(codigo_ibge="2501807", nome="Bananeiras", uf="PB", latitude=-6.75500, longitude=-35.6331),
    MunicipioIBGE(codigo_ibge="2505501", nome="Conceição", uf="PB", latitude=-7.55889, longitude=-38.5089),
    MunicipioIBGE(codigo_ibge="2511202", nome="Piancó", uf="PB", latitude=-7.19889, longitude=-37.9289),
    MunicipioIBGE(codigo_ibge="2507200", nome="Itaporanga", uf="PB", latitude=-7.30389, longitude=-38.1500),
    MunicipioIBGE(codigo_ibge="2516409", nome="Sumé", uf="PB", latitude=-7.67194, longitude=-36.8800)
]

class IbgeService:
    """Serviço de consulta e georreferenciamento de municípios."""

    def __init__(self):
        self._by_code: Dict[str, MunicipioIBGE] = {}
        self._by_name_uf: Dict[str, MunicipioIBGE] = {}
        for m in MUNICIPIOS_PARAIBA_REFERENCIA:
            self._by_code[m.codigo_ibge] = m
            self._by_name_uf[f"{m.nome.lower()}_{m.uf.lower()}"] = m

    def get_by_code(self, codigo_ibge: str) -> Optional[MunicipioIBGE]:
        return self._by_code.get(str(codigo_ibge).strip())

    def get_by_name(self, nome: str, uf: str = "PB") -> Optional[MunicipioIBGE]:
        key = f"{nome.strip().lower()}_{uf.strip().lower()}"
        return self._by_name_uf.get(key)

    def list_all_pilot(self) -> List[MunicipioIBGE]:
        return list(self._by_code.values())

    @staticmethod
    def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula a distância do grande círculo em quilômetros entre dois pontos
        utilizando a fórmula de Haversine.
        """
        raio_terra_km = 6371.0
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return raio_terra_km * c
