import pandas as pd
import numpy as np
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent.parent
DATA_DIR      = BASE_DIR / 'datasets'
RAW_DIR       = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'

FILE_PRODUTOS           = RAW_DIR       / 'produtos_raw.csv'
FILE_PRODUTOS_PROCESSED = PROCESSED_DIR / 'produtos_processed.csv'

# ── Questão 2 ──────────────────────────────────────────────────────────────────

produtos_2 = pd.read_csv(FILE_PRODUTOS, skip_blank_lines=False)

print(produtos_2.head())

# Isso vai listar todas as formas únicas que estão escritas na coluna e quantas vezes aparecem.
print(produtos_2['actual_category'].value_counts(dropna=False))

# Transformamos tudo em texto minúsculo e removemos todos os espaços em branco
produtos_2['actual_category'] = produtos_2['actual_category'].astype(str).str.lower().str.replace(' ', '', regex=False)

# Mapeamento Inteligente por Padrões (Regras de busca)
# Se a string contiver esse "pedaço" de palavra, ele classifica corretamente
condicoes = [
    produtos_2['actual_category'].str.contains('eletr', na=False), # Pega eletronicos, eletrunicos, eletronicoz...
    produtos_2['actual_category'].str.contains('prop', na=False),  # Pega propulsao, propução, prop...
    produtos_2['actual_category'].str.contains('ncor', na=False)   # Pega ancoragem, encoragem, ancorajm...
]

# Os nomes oficiais que queremos aplicar
categorias_oficiais = ['eletrônicos', 'propulsão', 'ancoragem']

# Aplica a regra usando np.select
# Se o texto não se encaixar em nenhuma regra, ele vira 'outros'
produtos_2['actual_category'] = np.select(condicoes, categorias_oficiais, default='outros')

# Prova real para garantir que funcionou perfeitamente
print(produtos_2['actual_category'].value_counts())

# Limpeza mais enxuta (apenas tirando R$ e espaços, mantendo o ponto original)
produtos_2['price'] = (
    produtos_2['price']
    .astype(str)                           
    .str.replace('R$', '', regex=False)    # Remove a letra R$
    .str.replace(' ', '', regex=False)     # Remove espaços em branco
    # Removemos aquelas linhas que trocavam o ponto e a vírgula!
)

# Conversão para numérico 
produtos_2['price'] = pd.to_numeric(produtos_2['price'], errors='coerce')

# Mostrar os primeiros 5 preços para garantir que os centavos ficaram no lugar certo
print(produtos_2['price'].head())

print(produtos_2['name'].value_counts(dropna=False))

# para garantir que os preços e códigos não sejam diferentes (ex: uma versão mais cara que a outra)
tabela_duplicatas = produtos_2[produtos_2.duplicated(subset=['name'], keep=False)].sort_values('name')
print("Linhas que estão duplicadas:\n", tabela_duplicatas)

# keep='first' Mantém a primeira vez que o produto apareceu e apaga as repetições abaixo
produtos_2 = produtos_2.drop_duplicates(subset=['name'], keep='first')

# Prova real
print(f"Total de linhas após limpeza: {produtos_2.shape[0]}") # Deve retornar 150

# Exporta o arquivo csv no diretorio de arquivos processados
produtos_2.to_csv(FILE_PRODUTOS_PROCESSED, index=False)
