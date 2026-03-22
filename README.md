# 📊 Análise de Vendas, Previsão e Sistema de Recomendação

Este repositório contém a resolução de um desafio técnico focado em extrair inteligência de negócio a partir de dados de vendas. O projeto aborda três pilares fundamentais da Ciência de Dados aplicada ao varejo: Previsão de Demanda (Series Temporais), Venda Cruzada (Sistemas de Recomendação) e Análise de Risco/Lucratividade (Visualização de Dados).

## 🎯 Objetivos do Projeto

1. **Previsão de Vendas (Baseline):** Estabelecer um modelo de previsão diária de vendas para janeiro de 2024 (foco no produto *Motor de Popa Yamaha Evo Dash 155HP*) utilizando a métrica MAE para avaliação.
2. **Motor de Recomendação:** Construir um sistema de Filtragem Colaborativa Baseada em Itens para sugerir produtos similares (foco no *GPS Garmin Vortex Maré Drift*), impulsionando estratégias de cross-sell.
3. **Análise de Prejuízos:** Mapear e visualizar os gargalos de lucratividade, identificando os produtos que mais drenam a margem da empresa através de gráficos interativos.

## 🛠️ Tecnologias e Bibliotecas Utilizadas

* **Linguagem:** Python 3
* **Manipulação de Dados:** `pandas`, `numpy`
* **Machine Learning & Métricas:** `scikit-learn` (Cosine Similarity, Mean Absolute Error)
* **Visualização de Dados:** `matplotlib`, `plotly.express`, `plotly.graph_objects`
* **Ambiente:** Jupyter Notebook

## 🧠 Destaques Técnicos e Decisões de Negócio

### 1. Modelo de Previsão (Moving Average)
* Implementação de um modelo *Baseline* utilizando Média Móvel de 7 dias para capturar a sazonalidade semanal de curto prazo.
* **Prevenção de Data Leakage:** Uso estrito do método `.shift(1)` para garantir que a previsão de um dia dependa unicamente do histórico anterior, simulando um ambiente de produção real.

### 2. Sistema de Recomendação (Cosine Similarity)
* Construção de uma matriz de interação Usuário x Produto baseada em dados binários (presença/ausência de compra), mitigando o viés de clientes atacadistas (outliers de volume).
* Cálculo de similaridade de cosseno vetorial para encontrar agrupamentos de interesse natural orgânico (Ex: clientes que compram o GPS alvo também compram os itens do Top 5 recomendado).

### 3. Visualização de Risco Analítico
* Transição de uma análise tabular densa (150 produtos com prejuízo) para Dashboards interativos em `.html`.
* **Treemap:** Para visualização imediata da proporção do prejuízo por produto.
* **Scatter Plot com Eixo X Invertido:** Cruzamento de % de Perda vs. Prejuízo Absoluto, facilitando a identificação da "zona de perigo" (produtos de alta receita, mas com margens destrutivas).

## 📁 Estrutura do Repositório

```text
├── database/                 # Instância local do banco de dados
│   
├── datasets/                 # Base de dados (CSV)
│   ├── raw/                  # Dados brutos de vendas
│   └── processed/            # Tabelas tratadas e padronizadas
│       └── output/           # Gráficos e exportações interativas
│           ├── treemap_prejuizo.html
│           └── scatter_prejuizo.html
│
├── notebooks/                # Código fonte
│   ├── resolucao_desafio.ipynb
│   ├── questao_2.py
│   ├── questao_3.py
│   ├── questao_7.py
│   └── questao_8.py
│
├── requirements.txt          # Dependências do projeto
├── .gitignore                # Arquivos ignorados no versionamento
└── README.md                 # Documentação do projeto