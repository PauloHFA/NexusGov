# Metodologia Analítica e Científica do NexusGov

O **NexusGov** fundamenta-se em princípios estatísticos, teoria dos grafos e ciência de redes complexas para triagem preventiva de compras públicas.

---

## 1. Eixo 1: Teoria dos Grafos (Empresa–Sócio–Licitação)
- **Modelo:** Grafo heterogêneo $G = (V, E)$ onde $V = \{E, S, L, A\}$:
  - $E$: Empresas licitantes
  - $S$: Sócios e administradores (QSA)
  - $L$: Licitações e certames
  - $A$: Atributos de contato (endereço canônico, telefone, e-mail)
- **Projeção de Coocorrência:** O grafo bipartido $E-S$ e $E-A$ é projetado em um grafo ponderado de empresas $G_E$, onde uma aresta existe se duas empresas compartilham sócio ou atributo.
- **Detecção de Comunidades:** Aplicação do algoritmo de **Leiden** (Traag et al., 2019) com particionamento baseado em modularidade ou otimização de CPM, eliminando comunidades desconexas e garantindo determinismo por semente pseudoaleatória fixa.
- **Métrica de Risco por Licitação ($RC$):**
  $$RC = \frac{\sum_{(u, v) \in P_L} w(u, v) \cdot \mathbb{I}(C(u) = C(v))}{|P_L|}$$
  onde $P_L$ é o conjunto de pares de empresas que disputaram a licitação $L$, e $\mathbb{I}$ indica se pertencem à mesma comunidade.
- **Controle por Grafo Nulo:** Comparação de $RC$ contra uma distribuição esperada em modelo de configuração nulo (preservando graus de conectividade) para evitar falsos positivos em pequenos municípios com poucos fornecedores locais.

---

## 2. Eixo 2: Lei de Benford
- **Distribuição Esperada:** O primeiro dígito significativo $d \in \{1, \dots, 9\}$ satisfaz:
  $$P(d) = \log_{10}\left(1 + \frac{1}{d}\right)$$
- **Critérios de Aplicabilidade Estritos:** Avaliado exclusivamente para amostras com $n \ge 300$ observações e amplitude de ao menos duas ordens de grandeza. Abaixo desse limiar, a saída é classificada como **"Não Aplicável"**, jamais como "Conforme".
- **Métricas:**
  - Desvio Médio Absoluto (*Mean Absolute Deviation - MAD* de Nigrini):
    $$MAD = \frac{1}{9}\sum_{d=1}^{9} |O_d - E_d|$$
    Limiares: $\le 0.006$ (próximo); $0.006 - 0.012$ (aceitável); $0.012 - 0.015$ (marginal); $> 0.015$ (não conforme).
  - Kolmogorov-Smirnov sobre a mantissa contínua:
    $$F(x) = \log_{10}(x) \pmod 1, \quad x > 0$$
  - Correção de Benjamini-Hochberg (FDR) em testes simultâneos múltiplos.

---

## 3. Eixo 3: Fracionamento de Despesa (Clusterização Temporal 1D)
- **Agrupamento:** Partição das compras diretas (dispensas de licitação) por tupla:
  $$(\text{órgão}, \text{fornecedor}, \text{código CATMAT/classe})$$
- **Janelas Deslizantes:** Varredura em horizontes móveis de 30, 60 e 90 dias.
- **Sinalização:** Sinal ativado quando o somatório dos valores contratados na janela superar o teto legal da modalidade vigente na data da contratação, ou quando houver $\ge 3$ dispensas sucessivas no intervalo com valor entre $80\%$ e $100\%$ do teto.

---

## 4. Eixo 4: Empresas Recém-Criadas (*Pop-up Vendors*)
- **Indicadores:**
  1. Idade do CNPJ no momento da abertura do edital (em dias).
  2. Razão entre valor adjudicado e capital social declarado.
  3. Distância geodésica entre a sede da empresa e o município contratante (via centróide IBGE).
  4. Compatibilidade da atividade econômica principal (CNAE) com o objeto licitado.

---

## 5. Índice de Exposição a Anomalias (IEA) e Salvaguardas
- **Cálculo:**
  $$IEA = 100 \times \frac{\sum_{i=1}^m w_i \cdot s_i \cdot c_i}{\sum_{i=1}^m w_i}$$
  onde $s_i \in [0, 1]$ é a intensidade do sinal $i$, $w_i > 0$ é o peso parametrizado da versão, e $c_i \in [0, 1]$ é o fator de confiança da evidência.
- **Níveis de Risco:**
  - **Baixo:** $IEA < 30$
  - **Médio:** $30 \le IEA \le 60$
  - **Elevado:** $IEA > 60$
- **Restrição Mandatória (SG-04):** O nível **"Elevado"** exige a confluência de no mínimo **dois sinais independentes de eixos distintos**. Se um único sinal for alto isoladamente, o teto é travado em **"Médio"**.
