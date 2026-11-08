"""
NexusGov - Coletor da API REST do Portal Nacional de Contratações Públicas (PNCP)
Requisitos: RF-ING-01, RF-ING-02, RNF-15 (Critérios de Aceite: CA-ING-01-A, CA-ING-02)
"""

import asyncio
from datetime import datetime
from typing import Any, AsyncGenerator, Dict, List, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from ..models.payloads import PncpContratacao, PncpItem, RawEvidence
from ..storage.raw_storage import RawStorageManager

class PncpRateLimitException(Exception):
    """Exceção levantada quando a API do PNCP retorna HTTP 429 (Too Many Requests)."""
    pass

class PncpCollector:
    """
    Cliente de coleta do PNCP com paginação, backoff exponencial, limitação de taxa
    e persistência imutável de payload bruto com hash SHA-256.
    """

    BASE_URL = "https://pncp.gov.br/api/consulta/v1"

    def __init__(
        self,
        raw_storage: Optional[RawStorageManager] = None,
        requests_per_second: float = 2.0,
        timeout_seconds: float = 30.0,
        transport: Optional[httpx.AsyncBaseTransport] = None,
        fetch_page_fn: Optional[Any] = None
    ):
        self.raw_storage = raw_storage or RawStorageManager()
        self.requests_per_second = requests_per_second
        self.timeout_seconds = timeout_seconds
        self.transport = transport
        self.fetch_page_fn = fetch_page_fn
        self._delay_between_requests = 1.0 / requests_per_second if requests_per_second > 0 else 0.5

    @retry(
        retry=retry_if_exception_type((httpx.RequestError, PncpRateLimitException)),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1.5, min=2, max=30),
        reraise=True
    )
    async def _fetch_page(
        self,
        client: httpx.AsyncClient,
        url: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executa requisição GET assíncrona com backoff exponencial se houver erro ou rate limiting (RF-ING-01).
        """
        await asyncio.sleep(self._delay_between_requests)
        response = await client.get(url, params=params, timeout=self.timeout_seconds)

        if response.status_code == 429:
            raise PncpRateLimitException("Limite de taxa do PNCP excedido (HTTP 429)")

        response.raise_for_status()
        return response.json()

    def parse_payload_to_contratacoes(
        self,
        payload: Dict[str, Any],
        competencia: str,
        uf: str = "PB",
        pagina: int = 1
    ) -> List[PncpContratacao]:
        """
        Processa um payload do PNCP, persiste a evidência forense bruta com SHA-256 (RF-ING-02)
        e retorna as contratações normalizadas.
        """
        registros = payload.get("data", [])
        if not registros and isinstance(payload, list):
            registros = payload

        contratacoes: List[PncpContratacao] = []
        for reg in registros:
            numero_controle = reg.get("numeroControlePNCP", f"TEMP_{pagina}_{reg.get('sequencialCompra', '0')}")
            url_registro = f"{self.BASE_URL}/contratacoes/{numero_controle}"

            evidence = self.raw_storage.store(
                identifier=numero_controle,
                url_fonte=url_registro,
                competencia=competencia,
                content=reg,
                uf=uf
            )
            contratacao = self._parse_to_model(reg, uf, evidence)
            contratacoes.append(contratacao)

        return contratacoes

    def collect_contratacoes_sync(
        self,
        data_inicial: str,
        data_final: str,
        uf: str = "PB",
        codigo_modalidade: Optional[int] = None,
        max_paginas: int = 50,
        sync_fetch_fn: Optional[Any] = None
    ) -> List[PncpContratacao]:
        """
        Coleta contratações de forma síncrona (adequada para workers em lote e testes).
        """
        competencia = f"{data_inicial[:4]}-{data_inicial[4:6]}"
        todas: List[PncpContratacao] = []
        pagina = 1

        while pagina <= max_paginas:
            params: Dict[str, Any] = {
                "dataInicial": data_inicial,
                "dataFinal": data_final,
                "uf": uf.upper(),
                "pagina": pagina,
                "tamanhoPagina": 50
            }
            if codigo_modalidade is not None:
                params["codigoModalidadeContratacao"] = codigo_modalidade

            if sync_fetch_fn:
                payload = sync_fetch_fn(f"{self.BASE_URL}/contratacoes/publicacao", params)
            else:
                with httpx.Client(timeout=self.timeout_seconds) as client:
                    resp = client.get(f"{self.BASE_URL}/contratacoes/publicacao", params=params)
                    if resp.status_code == 429:
                        raise PncpRateLimitException("Limite de taxa excedido")
                    resp.raise_for_status()
                    payload = resp.json()

            contratacoes = self.parse_payload_to_contratacoes(payload, competencia=competencia, uf=uf, pagina=pagina)
            if not contratacoes:
                break
            todas.extend(contratacoes)

            total_paginas = payload.get("totalPaginas", pagina)
            if pagina >= total_paginas:
                break
            pagina += 1

        return todas

    async def collect_contratacoes_por_periodo(
        self,
        data_inicial: str, # YYYYMMDD
        data_final: str,   # YYYYMMDD
        uf: str = "PB",
        codigo_modalidade: Optional[int] = None,
        max_paginas: int = 50
    ) -> AsyncGenerator[PncpContratacao, None]:
        """
        Coleta contratações publicadas no PNCP para uma UF e período assincronamente,
        gerando evidências brutas imutáveis e objetos normalizados.
        """
        url = f"{self.BASE_URL}/contratacoes/publicacao"
        competencia = f"{data_inicial[:4]}-{data_inicial[4:6]}"

        headers = {
            "Accept": "application/json",
            "User-Agent": "NexusGov-Audit-Bot/1.0 (+https://github.com/nexusgov/nexusgov)"
        }

        async with httpx.AsyncClient(headers=headers, transport=self.transport) as client:
            pagina = 1
            while pagina <= max_paginas:
                params: Dict[str, Any] = {
                    "dataInicial": data_inicial,
                    "dataFinal": data_final,
                    "uf": uf.upper(),
                    "pagina": pagina,
                    "tamanhoPagina": 50
                }
                if codigo_modalidade is not None:
                    params["codigoModalidadeContratacao"] = codigo_modalidade

                try:
                    if self.fetch_page_fn:
                        payload = await self.fetch_page_fn(url, params)
                    else:
                        payload = await self._fetch_page(client, url, params)
                except Exception:
                    break

                contratacoes = self.parse_payload_to_contratacoes(payload, competencia=competencia, uf=uf, pagina=pagina)
                if not contratacoes:
                    break

                for c in contratacoes:
                    yield c

                total_paginas = payload.get("totalPaginas", pagina)
                if pagina >= total_paginas:
                    break
                pagina += 1

    def _parse_to_model(self, raw: Dict[str, Any], uf: str, evidence: RawEvidence) -> PncpContratacao:
        """Mapeia o payload bruto da API do PNCP para o modelo PncpContratacao."""
        orgao = raw.get("orgaoEntidade", {}) or {}
        unidade = raw.get("unidadeOrgao", {}) or {}

        dt_abertura = self._safe_parse_datetime(raw.get("dataAberturaProposta"))
        dt_homologacao = self._safe_parse_datetime(raw.get("dataEncerramentoProposta") or raw.get("dataPublicacaoPncp"))

        itens_list: List[PncpItem] = []
        for raw_item in raw.get("itens", []) or []:
            itens_list.append(PncpItem(
                numero_item=raw_item.get("numeroItem", 1),
                descricao=raw_item.get("descricao", "Sem descrição"),
                codigo_catmat_catser=raw_item.get("codigoItemCatalogo"),
                quantidade=float(raw_item.get("quantidade", 1.0)),
                unidade_medida=raw_item.get("unidadeMedida"),
                valor_unitario_estimado=raw_item.get("valorUnitarioEstimado"),
                valor_unitario_homologado=raw_item.get("valorUnitarioHomologado"),
                valor_total=raw_item.get("valorTotal")
            ))

        return PncpContratacao(
            numero_controle_pncp=raw.get("numeroControlePNCP", evidence.id),
            orgao_cnpj=orgao.get("cnpj", "").replace(".", "").replace("/", "").replace("-", ""),
            orgao_nome=orgao.get("razaoSocial", "Órgão Não Informado"),
            esfera=orgao.get("esferaId", "MUNICIPAL"),
            poder=orgao.get("poderId", "EXECUTIVO"),
            uf=uf.upper(),
            codigo_ibge_municipio=unidade.get("municipioId"),
            modalidade_nome=raw.get("modalidadeNome", "Dispensa de Licitação"),
            numero_edital=raw.get("numeroCompra"),
            ano_compra=int(raw.get("anoCompra") or datetime.now().year),
            objeto=raw.get("objetoCompra", ""),
            valor_total_estimado=raw.get("valorTotalEstimado"),
            valor_total_homologado=raw.get("valorTotalHomologado"),
            data_abertura_proposta=dt_abertura,
            data_homologacao=dt_homologacao,
            situacao=raw.get("situacaoCompraNome"),
            url_pncp=raw.get("linkSistemaOrigem") or evidence.url_fonte,
            itens=itens_list
        )

    @staticmethod
    def _safe_parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
        if not dt_str:
            return None
        try:
            return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        except Exception:
            return None
