"""
Análise Exploratória de Dados - Higienização de dados dentro de um projeto
de ciência de dados: como lidar com dados reais?

Dataset: tv_shows.csv (programas de TV disponíveis em plataformas de streaming)
Disciplina: Análise Exploratória de Dados - Unidade 2
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Pasta onde os gráficos gerados serão salvos
PASTA_GRAFICOS = 'graficos'
os.makedirs(PASTA_GRAFICOS, exist_ok=True)

# =============================================================================
# 1. CARREGAMENTO DO DATASET
# =============================================================================

df = pd.read_csv('tv_shows.csv')

print("Dimensões do dataset:", df.shape)
print(df.head())

# =============================================================================
# 2. EXPLORAÇÃO DAS CARACTERÍSTICAS GERAIS DOS DADOS
# =============================================================================

# Equivalente ao str() do R: estrutura, tipos e não-nulos por coluna
print("\n--- Estrutura dos dados (df.info()) ---")
df.info()

# Equivalente ao summary() do R: resumo estatístico
print("\n--- Resumo estatístico (df.describe()) ---")
print(df.describe(include='all'))

# Contagem de valores nulos por coluna
print("\n--- Valores nulos por coluna ---")
print(df.isnull().sum())

# =============================================================================
# 3. IDENTIFICAÇÃO DE PROBLEMAS E HIGIENIZAÇÃO
# =============================================================================

linhas_antes = len(df)

# 3.1 Remover colunas irrelevantes para a análise
#     - 'Unnamed: 0': índice duplicado que vem do CSV
#     - 'Type': valor constante (não discrimina nada)
df = df.drop(columns=['Unnamed: 0', 'Type'])

# 3.2 Verificar e remover duplicatas (por Título + Ano)
duplicatas = df.duplicated(subset=['Title', 'Year']).sum()
print(f"\nDuplicatas encontradas (Título + Ano): {duplicatas}")
df = df.drop_duplicates(subset=['Title', 'Year'])

# 3.3 Tratar valores nulos
#     'Age' e 'IMDb' são centrais para a análise (classificação etária e
#     avaliação do público), então linhas sem esses dados são removidas.
nulos_age = df['Age'].isnull().sum()
nulos_imdb = df['IMDb'].isnull().sum()
print(f"Nulos em 'Age': {nulos_age} | Nulos em 'IMDb': {nulos_imdb}")

df = df.dropna(subset=['Age', 'IMDb'])

linhas_depois = len(df)
linhas_excluidas = linhas_antes - linhas_depois
print(f"\nLinhas antes da limpeza: {linhas_antes}")
print(f"Linhas depois da limpeza: {linhas_depois}")
print(f"Total de linhas excluídas: {linhas_excluidas}")

# =============================================================================
# 4. PADRONIZAÇÃO DOS DADOS
# =============================================================================

# 4.1 Converter 'IMDb' de texto ("9.4/10") para número (float)
df['IMDb'] = df['IMDb'].str.replace('/10', '', regex=False).astype(float)

# 4.2 Converter 'Rotten Tomatoes' de texto ("100/100") para número (int)
df['Rotten Tomatoes'] = df['Rotten Tomatoes'].str.replace('/100', '', regex=False).astype(int)

# 4.3 Converter 'Age' (classificação americana) para classificação indicativa
#     brasileira (Ministério da Justiça)
mapa_idade = {
    'all': 'Livre',
    '7+':  '10',
    '13+': '12',
    '16+': '16',
    '18+': '18',
}
df['Classificacao_BR'] = df['Age'].map(mapa_idade)

print("\n--- Amostra da padronização de classificação indicativa ---")
print(df[['Age', 'Classificacao_BR']].drop_duplicates())

# =============================================================================
# 5. ORGANIZAÇÃO DOS DADOS
# =============================================================================

# Ordenar os programas de TV pela nota do Rotten Tomatoes (decrescente)
df_ordenado = df.sort_values('Rotten Tomatoes', ascending=False).reset_index(drop=True)

# Número de plataformas em que cada título está disponível
df_ordenado['N_Plataformas'] = df_ordenado[
    ['Netflix', 'Hulu', 'Prime Video', 'Disney+']
].sum(axis=1)

print("\n--- Top 10 programas por nota do Rotten Tomatoes ---")
print(df_ordenado[['Title', 'Year', 'Rotten Tomatoes', 'IMDb', 'N_Plataformas']].head(10))

# 5.1 Ordenar os programas dentro de cada uma das 4 plataformas

plataformas = ['Netflix', 'Hulu', 'Prime Video', 'Disney+']
ranking_por_plataforma = {}

for plataforma in plataformas:
    sub = df_ordenado[df_ordenado[plataforma] == 1].sort_values(
        'Rotten Tomatoes', ascending=False
    ).reset_index(drop=True)
    ranking_por_plataforma[plataforma] = sub
    print(f"\n--- {plataforma} ({len(sub)} títulos) - Top 5 por Rotten Tomatoes ---")
    print(sub[['Title', 'Year', 'Rotten Tomatoes', 'IMDb']].head(5).to_string(index=False))

# =============================================================================
# 6. VISUALIZAÇÃO DOS DADOS
# =============================================================================

top15 = df_ordenado.head(15).sort_values('Rotten Tomatoes')

fig, ax = plt.subplots(figsize=(9, 6))
barras = ax.barh(top15['Title'], top15['Rotten Tomatoes'], color='#1f6feb')
ax.set_xlabel('Nota Rotten Tomatoes')
ax.set_title('Top 15 programas de TV por nota no Rotten Tomatoes')
ax.set_xlim(0, 105)

for barra, valor in zip(barras, top15['Rotten Tomatoes']):
    ax.text(valor + 1, barra.get_y() + barra.get_height() / 2, str(valor),
             va='center', fontsize=9)

plt.tight_layout()

caminho_grafico = os.path.join(PASTA_GRAFICOS, 'top15_rotten_tomatoes.png')
plt.savefig(caminho_grafico, dpi=150)
print(f"\nGráfico salvo em: {os.path.abspath(caminho_grafico)}")

plt.show()
plt.close(fig)

# =============================================================================
# 7. ANÁLISE DOS RESULTADOS
# =============================================================================

# 7.1 Quantas linhas necessitaram ser excluídas?
print(f"\n[Pergunta 1] Linhas excluídas: {linhas_excluidas} "
      f"({linhas_excluidas / linhas_antes:.1%} do total original)")

# 7.2 Programas com notas mais altas x mais baixas: em quantas plataformas?
top10 = df_ordenado.head(10)
bottom10 = df_ordenado.tail(10)
top100 = df_ordenado.head(100)
bottom100 = df_ordenado.tail(100)

print(f"\n[Pergunta 2] Média de plataformas - Top 10 (melhores notas): "
      f"{top10['N_Plataformas'].mean():.2f}")
print(f"[Pergunta 2] Média de plataformas - Bottom 10 (piores notas): "
      f"{bottom10['N_Plataformas'].mean():.2f}")
print(f"[Pergunta 2] Média de plataformas - Top 100: "
      f"{top100['N_Plataformas'].mean():.2f}")
print(f"[Pergunta 2] Média de plataformas - Bottom 100: "
      f"{bottom100['N_Plataformas'].mean():.2f}")

# 7.3 Ranking dos melhores programas de TV
print("\n[Pergunta 3] Ranking dos 10 melhores programas (Rotten Tomatoes):")
print(df_ordenado[['Title', 'Year', 'Rotten Tomatoes', 'IMDb']].head(10).to_string(index=False))

# =============================================================================
# 8. EXPORTAR DADOS TRATADOS (opcional, útil para o relatório)
# =============================================================================

df_ordenado.to_csv('tv_shows_tratado.csv', index=False)
print("\nDataset tratado exportado para 'tv_shows_tratado.csv'.")