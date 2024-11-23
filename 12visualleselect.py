import pandas as pd
from sklearn.decomposition import PCA
import numpy as np

# Configurações
input_geral = "musicas_emocoesGERAL.csv"  # Arquivo com mais de 1000 itens
input_jackson = "classificacoes_musicaJACKSON.csv"  # Arquivo com os dados de JACKSON
output_html = "pca_visualizacao_comparativo.html"

# Paleta de cores para emoções (baseada no `music.html`)
paleta_cores = {
    'Amusing': '#F9A825', 'Angry': '#D32F2F', 'Annoying': '#F57C00', 'Anxious': '#0288D1',
    'Awe-inspiring': '#512DA8', 'Beautiful': '#8E24AA', 'Bittersweet': '#AD1457', 'Calm': '#388E3C',
    'Compassionate': '#C2185B', 'Dreamy': '#7B1FA2', 'Eerie': '#424242', 'Energizing': '#FBC02D',
    'Entrancing': '#0097A7', 'Erotic': '#E64A19', 'Euphoric': '#1976D2', 'Exciting': '#0288D1',
    'Goose bumps': '#C62828', 'Indignant': '#BF360C', 'Joyful': '#FFC107', 'Nauseating': '#6D4C41',
    'Painful': '#795548', 'Proud': '#FFD600', 'Romantic': '#D81B60', 'Sad': '#1565C0',
    'Scary': '#616161', 'Tender': '#FF5722', 'Transcendent': '#4527A0', 'Triumphant': '#FFAB00'
}

# Ler os arquivos CSV
df_geral = pd.read_csv(input_geral)
df_jackson = pd.read_csv(input_jackson)

# Separar as colunas de emoções
emocoes_geral = df_geral.iloc[:, 1:]
emocoes_jackson = df_jackson.iloc[:, 1:]

# Identificar as emoções predominantes
df_geral['Emocao_Predominante'] = emocoes_geral.idxmax(axis=1)
df_jackson['Emocao_Predominante'] = emocoes_jackson.idxmax(axis=1)

# Normalizar os dados
emocoes_geral_normalizadas = emocoes_geral / emocoes_geral.max()
emocoes_jackson_normalizadas = emocoes_jackson / emocoes_jackson.max()

# Combinar os dados para o PCA
dados_combinados = pd.concat([emocoes_geral_normalizadas, emocoes_jackson_normalizadas])

# Aplicar PCA para reduzir as emoções para 2 dimensões
pca = PCA(n_components=2)
coordenadas_combinadas = pca.fit_transform(dados_combinados)

# Dividir as coordenadas entre os dois conjuntos
coordenadas_geral = coordenadas_combinadas[:len(df_geral)]
coordenadas_jackson = coordenadas_combinadas[len(df_geral):]

# Adicionar coordenadas aos DataFrames
df_geral['X'], df_geral['Y'] = coordenadas_geral[:, 0], coordenadas_geral[:, 1]
df_jackson['X'], df_jackson['Y'] = coordenadas_jackson[:, 0], coordenadas_jackson[:, 1]

# Gerar o HTML com visualização
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualização PCA Comparativa</title>
    <style>
        .ponto {
            position: absolute;
            border-radius: 50%;
            width: 14px;
            height: 14px;
            text-align: center;
            line-height: 14px;
            font-size: 10px;
            font-weight: bold;
            color: white;
        }
        .quadrado {
            position: absolute;
            width: 20px;
            height: 20px;
            text-align: center;
            line-height: 20px;
            font-size: 10px;
            font-weight: bold;
            color: white;
            border: 2px solid white; /* Argola */
        }
        #container {
            position: relative;
            width: 800px;
            height: 600px;
            border: 1px solid white;
            background-color: #000000; /* Fundo escuro */
        }
        svg {
            position: absolute;
            top: 0;
            left: 0;
        }
    </style>
</head>
<body>
    <h1 style="color: white;">Comparação PCA: GERAL vs JACKSON</h1>
    <div id="container">
        <svg width="800" height="600">
"""

# Normalizar coordenadas para caber no contêiner (800x600 px)
for df in [df_geral, df_jackson]:
    df['X_norm'] = (df['X'] - df['X'].min()) / (df['X'].max() - df['X'].min()) * 800
    df['Y_norm'] = (df['Y'] - df['Y'].min()) / (df['Y'].max() - df['Y'].min()) * 600

# Adicionar linhas conectando os pontos de JACKSON
for i in range(len(df_jackson) - 1):
    x1, y1 = df_jackson.iloc[i][['X_norm', 'Y_norm']]
    x2, y2 = df_jackson.iloc[i + 1][['X_norm', 'Y_norm']]
    html += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#00BFFF" stroke-width="2" />'

# Adicionar pontos do GERAL ao HTML
for _, row in df_geral.iterrows():
    emocao = row['Emocao_Predominante']
    cor = paleta_cores.get(emocao, '#FFFFFF')  # Branco como fallback
    letra = emocao[0].upper()
    html += f"""
        <div class="ponto" style="top: {row['Y_norm']}px; left: {row['X_norm']}px; background-color: {cor};" 
             title="GERAL | Emoção: {emocao}">
            {letra}
        </div>
    """

# Adicionar quadrados de JACKSON ao HTML
for i, row in df_jackson.iterrows():
    emocao = row['Emocao_Predominante']
    letra = str(i)  # Índice como texto
    html += f"""
        <div class="quadrado" style="top: {row['Y_norm']}px; left: {row['X_norm']}px; background-color: #00BFFF;" 
             title="JACKSON | Emoção: {emocao}">
            {letra}
        </div>
    """

html += """
        </svg>
    </div>
</body>
</html>
"""

# Salvar o arquivo HTML
with open(output_html, "w", encoding="utf-8") as file:
    file.write(html)

print(f"Arquivo HTML gerado: {output_html}")