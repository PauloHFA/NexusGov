# ADR-002: Estratégia de Identidade e Homonímia de Sócios

## Status
Aprovado

## Contexto
A base pública de CNPJs e Quadro de Sócios e Administradores (QSA) da Receita Federal disponibiliza os CPFs de sócios pessoas físicas com máscara de privacidade (apenas os 6 dígitos centrais: `***123456**`). Nomes comuns no Brasil (ex.: "José da Silva", "Maria de Souza") frequentemente geram colisões de homonímia, o que poderia provocar falsos positivos gravíssimos de cartéis ou coligações societárias caso tratados ingenuamente.
A LGPD (Lei 13.709/2018) proíbe expressamente tentativas de reidentificação ou desmascaramento de dados protegidos.

## Decisão
Implementar um modelo de **Identidade Probabilística com Nível de Confiança Ponderado ($c_i \in [0, 1]$)** e salvaguardas invioláveis:
1. **Chave de Fusão Primária:** `(nome_normalizado, cpf_mascarado)`. Quando dois sócios possuem idêntico nome normalizado e idênticos 6 dígitos mascarados, a confiança base é atribuída entre $0.70$ e $0.85$.
2. **Fatores de Aumento de Confiança:**
   - Compartilhamento de endereço corporativo idêntico: $+0.15$
   - Compartilhamento de telefone ou e-mail de contato cadastrado: $+0.15$
3. **Fatores de Redução de Confiança (Homonímia Alta):**
   - Sobrenomes de altíssima frequência no Brasil sem outros atributos compartilhados: confiança rebaixada para $\le 0.40$.
   - Parentesco presumido por sobrenome: peso fixado em $0.10$ e desligado por padrão no perfil conservador.
4. **Regra Inviolável SG-05:** Ligações societárias com confiança baseada unicamente em homonímia ou sobrenome comum jamais poderão elevar a classificação do edital para o nível "Elevado", limitando-se ao teto de "Médio".
5. **Rótulo Explícito na UI e API:** O vínculo é publicamente rotulado como "identidade presumida" com seu respectivo score de confiança visível.

## Consequências
- **Positivas:** Conformidade estrita com a LGPD; redução drástica de falsos positivos reputacionais; transparência na incerteza estatística.
- **Negativas:** Exige calibração empírica dos fatores de confiança e dicionário de nomes/sobrenomes frequentes.
