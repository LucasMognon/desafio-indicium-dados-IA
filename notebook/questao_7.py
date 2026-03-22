import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent.parent
DATA_DIR      = BASE_DIR / 'datasets'
PROCESSED_DIR = DATA_DIR / 'processed'

FILE_VENDAS_NORMALIZADA = PROCESSED_DIR / 'vendas_normalizadas.csv'
FILE_PRODUTOS_PROCESSED = PROCESSED_DIR / 'produtos_processed.csv'

# ── Questão 7 ──────────────────────────────────────────────────────────────────

# Carregar e Filtrar os Dados
vendas7   = pd.read_csv(FILE_VENDAS_NORMALIZADA)
produtos7 = pd.read_csv(FILE_PRODUTOS_PROCESSED)

df_completo = pd.merge(vendas7, produtos7, left_on='id_product', right_on='code', how='inner')
df_motor = df_completo[df_completo['name'] == 'Motor de Popa Yamaha Evo Dash 155HP'].copy()
df_motor['sale_date'] = pd.to_datetime(df_motor['sale_date'], format='mixed', dayfirst=True)

# Criar a Série Contínua (Preenchendo os dias sem venda com 0)
vendas_diarias = df_motor.groupby('sale_date')['qtd'].sum().reset_index()

data_min  = vendas_diarias['sale_date'].min()
data_max  = pd.to_datetime('2024-01-31')
calendario = pd.DataFrame({'sale_date': pd.date_range(start=data_min, end=data_max)})

serie_completa = pd.merge(calendario, vendas_diarias, on='sale_date', how='left').fillna(0)
serie_completa = serie_completa.sort_values('sale_date')

# Criando modelo de média móvel (BASELINE)
# shift(1): Pega o dado do dia anterior (Garante que não há data leakage)
# rolling(7): Pega a janela dos últimos 7 dias
# mean(): Calcula a média dessa janela
serie_completa['previsao_ma7'] = serie_completa['qtd'].shift(1).rolling(window=7).mean()

# Arredondando porque não vendemos "meio" motor
# O fillna(0) trata os primeiros 7 dias de 2023 que ficarão vazios por falta de histórico anterior
serie_completa['previsao_ma7'] = np.round(serie_completa['previsao_ma7'].fillna(0))

# Split treino/teste
# Isolamos apenas Janeiro de 2024 para o teste
teste  = serie_completa[(serie_completa['sale_date'] >= '2024-01-01') & 
                        (serie_completa['sale_date'] <= '2024-01-31')].copy()

treino = serie_completa[serie_completa['sale_date'] <= '2023-12-31'].copy()

# Mean Absolute Error (Erro Médio Absoluto)
mae_ma7 = mean_absolute_error(teste['qtd'], teste['previsao_ma7'])

# visualização dos resultados
plt.figure(figsize=(16, 6))

plt.plot(treino['sale_date'][-60:], treino['qtd'][-60:], label='Histórico (Treino 2023)', color='gray', alpha=0.6)
plt.plot(teste['sale_date'], teste['qtd'], label='Realidade (Teste: Jan/2024)', color='blue', marker='o')
plt.plot(teste['sale_date'], teste['previsao_ma7'], label='Previsão (Média Móvel 7 Dias)', color='red', linestyle='--', marker='x')

plt.title('Baseline: Média Móvel de 7 Dias (Yamaha Evo Dash 155HP)', fontsize=14)
plt.xlabel('Data')
plt.ylabel('Qtd Vendida (Unidades)')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()

# Resumo Final e Cálculo do MAE
print("-" * 50)
print(f"AVALIAÇÃO DO MODELO DE MÉDIA MÓVEL - JAN/2024")
print("-" * 50)
print(f"Total REAL vendido em Jan/24       : {teste['qtd'].sum():.0f} unidades")
print(f"Total PREVISTO pelo modelo (MA7)   : {teste['previsao_ma7'].sum():.0f} unidades")
print(f"Métrica MAE (Mean Absolute Error)  : {mae_ma7:.2f} unidades de erro por dia")
