# Salvaguardas Metodológicas e Éticas Invioláveis (SG)

Estas regras representam restrições mandatórias de sistema. Qualquer alteração em seu comportamento exige aprovação jurídica e revisão do comitê de ética/projeto.

## SG-01: Linguagem Não Acusatória e Neutra
- **Prioridade:** Inviolável (Must)
- **Descrição:** A interface de usuário, os relatórios gerados em PDF, a documentação OpenAPI e os payloads das respostas da API NUNCA utilizam termos como "fraude", "crime", "culpado" ou "conluio comprovado". Empregam-se com exclusividade **"indício"**, **"exposição"** e **"sinal"**.
- **Critério de Aceite (CA-SG-01):**
  - **Dado** qualquer arquivo de código-fonte de visualização, template de relatório PDF ou resposta serializada de API,
  - **Quando** o linter/scanner automatizado é executado,
  - **Então** 0 ocorrências de palavras proibidas são encontradas e a presença do aviso metodológico é confirmada.

## SG-02: Transparência e Rastreabilidade Total de Evidências
- **Prioridade:** Inviolável (Must)
- **Descrição:** Toda contratação classificada nos níveis "Médio" ou "Elevado" exibe de forma detalhada e auditável a relação de todos os sinais ativados que a compõem e suas evidências verificáveis.
- **Critério de Aceite (CA-SG-02-A):**
  - **Dado** um resultado de IEA $\ge 30$,
  - **Quando** inspecionado via API ou UI,
  - **Então** contém a decomposição discriminada dos sinais, os pesos da versão corrente e o link direto para a fonte original no PNCP.

## SG-03: Aviso Metodológico Obrigatório em Todas as Emissões
- **Prioridade:** Inviolável (Must)
- **Descrição:** Todo relatório impresso, arquivo exportado e tela de visualização contém o aviso metodológico padronizado e a identificação da versão do modelo estatístico e da tabela de parâmetros.
- **Critério de Aceite (CA-SG-03):**
  - **Dado** um dossiê PDF ou tela gerada,
  - **Quando** renderizado,
  - **Então** apresenta o aviso informando: "Os indicadores aqui apresentados constituem triagem probabilística e não representam juízo de mérito ou prova de irregularidade".

## SG-04: Exigência de Multieixo para Classificação de Risco Elevado
- **Prioridade:** Inviolável (Must)
- **Descrição:** Nenhuma contratação pode receber a classificação de nível "Elevado" ($IEA > 60$) sustentada por sinais de um único eixo analítico isolado. Exige-se a convergência de ao menos **dois sinais independentes de eixos distintos** (ex.: Grafo + Fracionamento; ou Grafo + Benford; ou Fracionamento + Pop-up Vendor).
- **Critério de Aceite (CA-SG-02):**
  - **Dado** uma contratação com pontuação aritmética alta em apenas 1 eixo isolado (ex.: sinal 1.0 em Benford, mas zero nos demais),
  - **Quando** o motor de cálculo do IEA processa o resultado,
  - **Então** o nível final é automaticamente truncado em "Médio", garantindo a salvaguarda de multieixo.

## SG-05: Proteção contra Falsos Positivos de Homonímia
- **Prioridade:** Inviolável (Must)
- **Descrição:** Vínculos societários identificados unicamente por nome comum de pessoa física ou parentesco presumido por sobrenome possuem confiança ponderada reduzida e NUNCA podem ser a base exclusiva para elevar o risco de uma licitação acima do nível "Médio".
- **Critério de Aceite (CA-SG-05):**
  - **Dado** dois sócios com mesmo sobrenome comum em empresas concorrentes, sem outros indícios de endereço ou telefone compartilhados,
  - **Quando** o risco de cartel é processado,
  - **Então** a confiança atribuída ao vínculo é baixa ($c_i \le 0.1$) e a classificação não ultrapassa o nível "Médio".
