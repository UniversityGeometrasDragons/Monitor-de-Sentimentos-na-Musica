import pandas as pd
from sklearn.decomposition import PCA

# Caminho do arquivo CSV
input_csv = "classificacoes_musicaTURKISH.csv"
output_html = "pca_visualizacao.html"

# Ler o arquivo CSV
df = pd.read_csv(input_csv)

# Separar as colunas de emoções
emocoes = df.iloc[:, 1:]  # Todas as colunas a partir da segunda (emoções)
tempos = df['Trecho_Inicial']  # Coluna de tempo

# Identificar a emoção predominante em cada trecho
emocoes_predominantes = emocoes.idxmax(axis=1)
df['Emocao_Predominante'] = emocoes_predominantes

# Normalizar as emoções para melhorar o PCA
emocoes_normalizadas = emocoes / emocoes.max()

# Aplicar PCA para reduzir as emoções para 2 dimensões
pca = PCA(n_components=2)
coordenadas = pca.fit_transform(emocoes_normalizadas)

# Adicionar as coordenadas calculadas ao DataFrame original
df['X'] = coordenadas[:, 0]
df['Y'] = coordenadas[:, 1]

# Paleta de cores para as emoções
paleta_cores = {
    'Amusing': '#F9A825', 'Angry': '#D32F2F', 'Annoying': '#F57C00', 'Anxious': '#0288D1',
    'Awe-inspiring': '#512DA8', 'Beautiful': '#8E24AA', 'Bittersweet': '#AD1457', 'Calm': '#388E3C',
    'Compassionate': '#C2185B', 'Dreamy': '#7B1FA2', 'Eerie': '#424242', 'Energizing': '#FBC02D',
    'Entrancing': '#0097A7', 'Erotic': '#E64A19', 'Euphoric': '#1976D2', 'Exciting': '#0288D1',
    'Goose bumps': '#C62828', 'Indignant': '#BF360C', 'Joyful': '#FFC107', 'Nauseating': '#6D4C41',
    'Painful': '#795548', 'Proud': '#FFD600', 'Romantic': '#D81B60', 'Sad': '#1565C0',
    'Scary': '#616161', 'Tender': '#FF5722', 'Transcendent': '#4527A0', 'Triumphant': '#FFAB00'
}

# Gerar o HTML para exibir os pontos
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualização PCA</title>
    <style>
        .ponto {
            position: absolute;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            text-align: center;
            line-height: 20px;
            font-size: 12px;
            font-weight: bold;
            color: white;
        }
        #container {
            position: relative;
            width: 800px;
            height: 600px;
            border: 1px solid black;
            background-color: #f5f5f5;
        }
        svg line {
            stroke: gray;
            stroke-width: 2;
        }
    </style>
</head>
<body>
    <h1>Visualização PCA das Emoções</h1>
    <div id="container">
        <svg width="800" height="600">
"""

# Normalizar X e Y para caber no contêiner de 800x600 px
df['X_norm'] = (df['X'] - df['X'].min()) / (df['X'].max() - df['X'].min()) * 800
df['Y_norm'] = (df['Y'] - df['Y'].min()) / (df['Y'].max() - df['Y'].min()) * 600

# Adicionar linhas conectando os pontos
for i in range(1, len(df)):
    x1, y1 = df.iloc[i - 1]['X_norm'], df.iloc[i - 1]['Y_norm']
    x2, y2 = df.iloc[i]['X_norm'], df.iloc[i]['Y_norm']
    html += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'

# Adicionar cada ponto ao HTML
for index, row in df.iterrows():
    emocao = row['Emocao_Predominante']
    cor = paleta_cores.get(emocao, '#000000')  # Preto como fallback para emoções sem cor
    letra = emocao[0].upper()  # Primeira letra da emoção
    html += f"""
        <div class="ponto" style="top: {row['Y_norm']}px; left: {row['X_norm']}px; background-color: {cor};" 
             title="Tempo: {row['Trecho_Inicial']} | Emoção: {emocao} | Índice: {index}">
            {letra} {index}
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