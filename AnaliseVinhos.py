import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
from scipy.stats import pearsonr

#Importação do CSV, correção dos países não informados e tema do Seaborn
df = pd.read_csv('winemag-data-130k-v2.csv')
df['country'].fillna('Não informado', inplace=True)
sns.set_style('darkgrid')
sns.color_palette("rocket")
df = df.dropna(subset=['price'])
df.dropna(subset=['region_1'])

#1 - Qual é o país com o maior número de vinhos no dataset?
'''
# Contar o número de vinhos por país
df_2 = pd.DataFrame(df['country'].value_counts().head(10))
df_2.columns = ['count']

# Exibir os valores
print(df['country'].value_counts())
print(df_2)

# Plotar o gráfico de barras
plt.figure(figsize=(12, 8))
sns.barplot(data=df_2, x='count', y=df_2.index, palette='magma')

# Adicionar título e rótulos com tamanho maior
plt.title('Top 10 Países com o Maior Número de Vinhos', fontsize=20)
plt.xlabel('Número de Vinhos', fontsize=16)
plt.ylabel('País', fontsize=16)

# Ajustar o tamanho dos ticks dos eixos
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Ajustar o layout e exibir o gráfico
plt.tight_layout()
plt.show()
'''
#2 - Qual é a média de pontos dos vinhos por país?
'''
sns.lineplot(
    data=df.groupby('country')['points'].mean().reset_index().sort_values(by='points'),
    x='country', y='points', marker='o', palette='orange'
)

# Ajustar tamanho das legendas e rótulos
plt.xticks(fontsize=20)  # Tamanho dos rótulos no eixo X
plt.yticks(fontsize=20)  # Tamanho dos rótulos no eixo Y
plt.title('Média de pontos dos vinhos por país', fontsize=30)  # Tamanho do título
plt.xlabel('Países', fontsize=25)  # Tamanho do rótulo do eixo X
plt.ylabel('Pontos', fontsize=25, labelpad=30)  # Tamanho do rótulo do eixo Y e espaço adicional

# Ajustar rotação e alinhamento dos rótulos do eixo X
plt.xticks(rotation=90, ha='right')

# Ajustar layout
plt.tight_layout()

# Exibir o gráfico
plt.show()
'''
# 3 - Existe uma correlação entre o preço e os pontos dos vinhos?
'''

coef, p_value = pearsonr(df['price'].dropna(), df['points'].dropna())

print(f"Coeficiente de correlação de Pearson: {coef:.2f}")
print(f"Valor p: {p_value:.4f}")

if p_value <= 0.05:
    print("Existe uma correlação significativa entre o preço e os pontos dos vinhos.")
else:
    print("Não há correlação significativa entre o preço e os pontos dos vinhos.")

'''
# 4 - Quais regiões têm os vinhos com as maiores classificações?
'''
# Agrupando por região e calculando a média de pontos
media_pontos = df.groupby('region_1')['points'].mean().reset_index()

# Ordenando pela média de pontos em ordem decrescente
media_pontos = media_pontos.sort_values(by='points', ascending=False)

print(media_pontos.head(5))
'''

#5 - Qual é a variedade de vinho mais comum no dataset?
'''
variedadeVinhos = df['variety'].value_counts()
print(variedadeVinhos.head(5))

ax = variedadeVinhos.head(10).plot(kind='barh', color='purple', figsize=(12, 8))

plt.title('Os 10 Vinhos Mais Comuns no Dataset', fontsize=30)
plt.xlabel('Quantidade', fontsize=25)
plt.ylabel('Variedade dos Vinhos', fontsize=25, labelpad=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xticks(rotation=45, ha='center')

for i, v in enumerate(variedadeVinhos.head(10)):
    ax.text(v + 1, i, str(v), va='center', ha='left', color='black', fontsize=18)

plt.tight_layout()
plt.show()

'''

#6 -Como o preço dos vinhos varia entre os diferentes países?

'''
# Remover valores nulos na coluna de preço
df = df.dropna(subset=['price'])

# Agrupar por país e calcular o preço médio dos vinhos
preco_medio_pais = df.groupby('country')['price'].mean().reset_index()

# Ordenar os países pelo preço médio
preco_medio_pais = preco_medio_pais.sort_values(by='price', ascending=False)

# Exibir as 10 primeiras linhas para verificar o resultado
print(preco_medio_pais.head(10))

# Criar o gráfico de barras horizontal para mostrar o preço médio dos vinhos por país
plt.barh(preco_medio_pais['country'], preco_medio_pais['price'], color='green')

# Configurar o gráfico
plt.title('Preço Médio dos Vinhos por País')
plt.xlabel('Preço Médio ($)')
plt.ylabel('País', labelpad=20)
plt.grid(axis='x')

# Adicionar o valor do preço médio na frente de cada barra
for i, v in enumerate(preco_medio_pais['price']):
    plt.text(v + 0.5, i, f"${v:.2f}", va='center', ha='left', color='black')

# Exibir o gráfico
plt.show()
'''

# 7 - Existe alguma tendência nos pontos dos vinhos ao longo dos anos?
'''
df['year'] = df['title'].str.extract(r'(\d{4})')

sns.set_theme()
sns.set_context("paper")
sns.color_palette("tab10")

# Converter a coluna 'year' para tipo numérico (caso algum valor não tenha sido extraído corretamente)
df['year'] = pd.to_numeric(df['year'], errors='coerce')

# Filtrar para considerar apenas anos válidos (ex: entre 1900 e 2024)
df = df[(df['year'] >= 1900) & (df['year'] <= 2024)]

# Verificar se há valores nulos e removê-los
df = df.dropna(subset=['year', 'points'])

# Calcular a média dos pontos por ano
avg_points_per_year = df.groupby('year')['points'].mean().reset_index()

# Gráfico de linha para mostrar a evolução dos pontos ao longo dos anos
plt.figure(figsize=(14, 8))
sns.lineplot(data=avg_points_per_year, x='year', y='points', marker='o')

# Adicionar título e rótulos aos eixos
plt.title('Evolução dos Pontos dos Vinhos ao Longo dos Anos', fontsize=16)
plt.xlabel('Ano', fontsize=14)
plt.ylabel('Pontuação Média', fontsize=14)

# Ajuste do gráfico
plt.grid(True)
plt.tight_layout()

# Exibir gráfico
plt.show()
'''

# 8 - Quais são os 5 vinhos com a maior pontuação?

'''
# Ordenar o DataFrame pela coluna 'points' em ordem decrescente (maiores pontuações primeiro)
vinhos_maior_pontuacao = df[['title', 'points',]].sort_values(by='points', ascending=False)

# Exibir as 10 primeiras linhas (top 19 vinhos com maior pontuação)
print(vinhos_maior_pontuacao.head(19))
'''

# 9 - Quais são os 5 vinhos com o menor preço?
'''
vinhos_menor_preco = df[['title', 'price']].sort_values(by='price', ascending=True)
print(vinhos_menor_preco.head(11))
'''

#14 - Quais vinhos têm a maior diferença entre a pontuação e o preço?

'''
# Ajustar configuração para exibir todas as colunas e mais linhas
pd.set_option('display.max_columns', None)  # Exibe todas as colunas
pd.set_option('display.max_rows', 20)      # Altere para None se quiser exibir todas as linhas

# Remover valores nulos nas colunas 'points' e 'price'
df = df.dropna(subset=['points', 'price'])

# Calcular a diferença entre pontuação e preço
df['diferencaPontosPreco'] = df['points'] - df['price']

# Selecionar as colunas relevantes e ordenar pela maior diferença
vinhos_maior_diferenca = df[['title', 'points', 'price', 'diferencaPontosPreco']].sort_values(by='diferencaPontosPreco', ascending=False)

# Exibir os 10 vinhos com maior diferença
print(vinhos_maior_diferenca.head(10))
'''

#18 - Quais são os 10 vinhos mais caros e suas respectivas pontuações?
'''
df = df.dropna(subset=['price'])

# Ordenar os vinhos pelo preço em ordem decrescente
vinhosMaisCaros = df[['title', 'price', 'points']].sort_values(by='price', ascending=False)


# Exibir o resultado
print(vinhosMaisCaros.head(10))
'''

#21 - Como o preço médio dos vinhos varia entre as diferentes regiões?
'''
# Remover valores nulos ou em branco nas colunas 'region_1' e 'price'
df = df.dropna(subset=['region_1', 'price'])

# Calcular o preço médio por região
preco_medio_regiao = df.groupby('region_1')['price'].mean().reset_index()

# Ordenar as regiões pelo preço médio
preco_medio_regiao = preco_medio_regiao.sort_values(by='price', ascending=False)

# Configurar o tamanho da figura
plt.figure(figsize=(12, 8))

# Criar o gráfico de barras com Seaborn
sns.barplot(
    data=preco_medio_regiao.head(10),  # Mostrar apenas as 10 principais regiões
    x='price',
    y='region_1',
    palette='viridis'
)

# Adicionar título e rótulos
plt.title('Top 10 Regiões com Maior Preço Médio de Vinhos', fontsize=16)
plt.xlabel('Preço Médio (USD)', fontsize=12)
plt.ylabel('Região', fontsize=12)

# Ajustar layout para uma melhor visualização
plt.tight_layout()

# Exibir o gráfico
plt.show()
'''

#22 - Quais vinhos são considerados os melhores em termos de custo-benefício (preço/pontuação)?
'''

# Configuração para exibir todas as colunas e mais linhas
pd.set_option('display.max_columns', None)  # Exibe todas as colunas
pd.set_option('display.max_rows', None)     # Exibe todas as linhas
pd.set_option('display.float_format', '{:.2f}'.format)  # Formata floats para 2 casas decimais

# Remover valores nulos em 'price' e 'points'
df = df.dropna(subset=['price', 'points'])

# Calcular a razão preço/pontuação
df['custo_beneficio'] = df['price'] / df['points']

# Ordenar os vinhos pela melhor razão (menor custo por ponto)
melhores_custo_beneficio = df[['title', 'points', 'price', 'custo_beneficio']].sort_values(by='custo_beneficio')

# Exibir os 10 vinhos com melhor custo-benefício
print(melhores_custo_beneficio.head(10))
'''

#27 - Como a pontuação dos vinhos varia entre diferentes degustadores?

# Remover valores nulos nas colunas 'taster_twitter_handle' e 'points'
df = df.dropna(subset=['taster_twitter_handle', 'points'])

# Calcular a pontuação média por degustador (Twitter handle)
pontuacao_por_degustador = df.groupby('taster_twitter_handle')['points'].mean().reset_index()

# Ordenar os degustadores pela pontuação média
pontuacao_por_degustador = pontuacao_por_degustador.sort_values(by='points', ascending=False)

# Configurar o tamanho do gráfico
plt.figure(figsize=(12, 6))

# Criar um gráfico de pontos (scatterplot) com eixos invertidos
sns.scatterplot(
    data=pontuacao_por_degustador,
    x='taster_twitter_handle',
    y='points',
    s=100,  # Tamanho dos pontos
    color='purple',
    edgecolor='black'
)

# Adicionar título e rótulos
plt.title('Pontuação Média dos Vinhos por Degustador (Twitter)', fontsize=16)
plt.ylabel('Pontuação Média', fontsize=12)
plt.xlabel('Degustador (Twitter)', fontsize=12)

# Ajustar rotação dos rótulos do eixo X
plt.xticks(rotation=45, ha='right', fontsize=20)
plt.yticks(fontsize=20)

# Adicionar grades para facilitar a leitura
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Ajustar layout
plt.tight_layout()

# Exibir o gráfico
plt.show()
