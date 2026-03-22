import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent.parent
DATA_DIR      = BASE_DIR / 'datasets'
RAW_DIR       = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'

FILE_VENDAS             = RAW_DIR       / 'vendas_2023_2024.csv'
FILE_PRODUTOS_PROCESSED = PROCESSED_DIR / 'produtos_processed.csv'

# ── Questão 8 ──────────────────────────────────────────────────────────────────

# Carregar as tabelas
vendas_8   = pd.read_csv(FILE_VENDAS)
produtos_8 = pd.read_csv(FILE_PRODUTOS_PROCESSED)

# Exibir uma mensagem de confirmação
print(f"Vendas carregadas: {vendas_8.shape[0]} linhas.")
print(f"Produtos carregados: {produtos_8.shape[0]} itens.")

# MATRIZ DE INTERAÇÃO (PRESENÇA/AUSÊNCIA)

# 1. Filtramos usando o novo DataFrame vendas_8 e removemos duplicatas
interacoes = vendas_8[['id_client', 'id_product']].drop_duplicates().copy()

# 2. Criamos uma coluna artificial chamada 'comprou' com o número 1
interacoes['comprou'] = 1

# 3. Criamos a Matriz Pivot
matriz_interacao = interacoes.pivot(
    index='id_client', 
    columns='id_product', 
    values='comprou'
).fillna(0)

print("Matriz de Interação criada com sucesso!")
print(f"Dimensões: {matriz_interacao.shape[0]} Clientes x {matriz_interacao.shape[1]} Produtos")
print(matriz_interacao.head())

# MATRIZ DE SIMILARIDADE DE COSSENO

# Transpor a matriz (Linhas viram produtos, colunas viram clientes)
matriz_produtos = matriz_interacao.T

# Calcular a similaridade matemática
similaridade_array = cosine_similarity(matriz_produtos)

# Transformar o resultado de volta em um DataFrame
df_similaridade = pd.DataFrame(
    similaridade_array,
    index=matriz_produtos.index,
    columns=matriz_produtos.index
)

print("Similaridade Produto x Produto calculada!")
print(df_similaridade.head())

# Ranking de recomendação top 5

NOME_ALVO = 'GPS Garmin Vortex Maré Drift'

# Descobrir o ID buscando no novo DataFrame produtos_8
id_alvo = produtos_8.loc[produtos_8['name'] == NOME_ALVO, 'code'].values[0]

# Pegar as similaridades apenas desse GPS e ordenar
similares_ao_alvo = df_similaridade[id_alvo].sort_values(ascending=False)

# Remover o próprio GPS da lista
similares_ao_alvo = similares_ao_alvo.drop(id_alvo)

# Pegar o Top 5
top_5_ids = similares_ao_alvo.head(5).reset_index()
top_5_ids.columns = ['id_product', 'score_similaridade']

# Fazer o JOIN com produtos_8 para trazer os nomes e categorias
ranking_final = pd.merge(
    top_5_ids, 
    produtos_8[['code', 'name', 'actual_category']], 
    left_on='id_product', 
    right_on='code', 
    how='left'
)

# Exibir o resultado final
print("-" * 60)
print(f" PRODUTO REFERÊNCIA: {NOME_ALVO}")
print("-" * 60)
print("Os 5 produtos mais recomendados para venda cruzada (Cross-Sell) são:\n")

# Formatando o score
ranking_final['score_similaridade'] = (ranking_final['score_similaridade'] * 100).round(2).astype(str) + '%'

print(ranking_final[['name', 'actual_category', 'score_similaridade']].to_string(index=False))
