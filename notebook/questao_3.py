import pandas as pd
import json
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent.parent
DATA_DIR      = BASE_DIR / 'datasets'
RAW_DIR       = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'

FILE_CUSTOS_JSON = RAW_DIR       / 'custos_importacao.json'
FILE_CUSTOS_NORM = PROCESSED_DIR / 'custos_importacao_normalizado.csv'

# ── Questão 3 ──────────────────────────────────────────────────────────────────

# Carregar o arquivo JSON
with open(FILE_CUSTOS_JSON, 'r', encoding='utf-8') as f:
    dados_json = json.load(f)

# Achatar (Normalizar) o JSON
df_importacao = pd.json_normalize(
    dados_json,
    record_path=['historic_data'],
    meta=['product_id', 'product_name', 'category']
)

# Reorganizar a ordem das colunas para bater com o seu requisito
df_importacao = df_importacao[['product_id', 'product_name', 'category', 'start_date', 'usd_price']]

# Garantir os tipos de dados (Tipagem forte)
df_importacao['product_id'] = df_importacao['product_id'].astype(int)
df_importacao['usd_price']  = df_importacao['usd_price'].astype(float)

# Converte a data no formato YYYY-MM-DD
df_importacao['start_date'] = pd.to_datetime(df_importacao['start_date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

# Exportar para o novo arquivo CSV com segurança de diretório
FILE_CUSTOS_NORM.parent.mkdir(parents=True, exist_ok=True)
df_importacao.to_csv(FILE_CUSTOS_NORM, index=False)

# Calculando numero de entradas de importação
total_entradas = df_importacao.shape[0]
print(f"Sucesso! O arquivo foi salvo em: {FILE_CUSTOS_NORM.resolve()}")
print(f"RESPOSTA: O CSV recebeu ao todo {total_entradas} entradas de importação após a normalização.")
