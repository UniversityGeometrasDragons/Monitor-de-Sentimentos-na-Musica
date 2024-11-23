import re
import pandas as pd

# Caminho do arquivo original
input_html = "music.html"

# Variáveis para armazenar os dados extraídos
dados = []

# Expressão regular para capturar as informações de cada item
regex = r'<div id=item(\d+).*?style="color: (#[0-9A-Fa-f]+); top: ([0-9.]+)px; left: ([0-9.]+)px.*?title=".*?">(.*?)</div>'

# Ler o arquivo HTML e processar
with open(input_html, "r", encoding="ISO-8859-1") as file:
    conteudo = file.read()
    matches = re.findall(regex, conteudo)
    for match in matches:
        item_id, cor, top, left, letra = match
        dados.append({
            "ID": int(item_id),
            "Cor": cor,
            "Y": float(top),
            "X": float(left),
            "Letra": letra
        })

# Converter os dados em DataFrame
df = pd.DataFrame(dados)

# Gerar um HTML para exibir os pontos PCA
output_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exibição PCA</title>
    <style>
        .ponto {
            position: absolute;
            border-radius: 50%;
            width: 10px;
            height: 10px;
            text-align: center;
            line-height: 10px;
            font-size: 10px;
            font-weight: bold;
        }
        #container {
            position: relative;
            width: 800px;
            height: 600px;
            border: 1px solid black;
        }
    </style>
</head>
<body>
    <div id="container">
"""

# Adicionar cada ponto no HTML
for _, row in df.iterrows():
    output_html += f"""
        <div class="ponto" style="background-color: {row['Cor']}; top: {row['Y']}px; left: {row['X']}px;">
            {row['Letra']}
        </div>
    """

output_html += """
    </div>
</body>
</html>
"""

# Salvar o novo arquivo HTML
with open("pca_visualizacao.html", "w", encoding="utf-8") as file:
    file.write(output_html)

print("Novo arquivo HTML gerado: pca_visualizacao.html")