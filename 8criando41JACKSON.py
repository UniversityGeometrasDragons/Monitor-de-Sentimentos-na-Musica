import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from pydub import AudioSegment
import librosa
import librosa.display
import matplotlib.pyplot as plt

# Caminhos
modelo_caminho = 'modelo_emocoesEUA.h5'  # Caminho para o modelo treinado
segmentos_dir = r'C:\base\EXPERIMENTO5\output_segments'  # Diretório com arquivos segment_X-Y.mp3
output_dir = r'C:\base\EXPERIMENTO5\EspecsTOT'  # Diretório temporário para salvar espectrogramas

# Carregar o modelo treinado
model = load_model(modelo_caminho)

# Garantir que o diretório de espectrogramas temporários exista
os.makedirs(output_dir, exist_ok=True)

# Função para converter um segmento de áudio em espectrograma e carregá-lo como imagem
def audio_para_espectrograma(input_file, output_file, img_size=(128, 128)):
    y, sr = librosa.load(input_file, sr=22050)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    
    # Salvar o espectrograma temporariamente
    plt.figure(figsize=(img_size[0]/100, img_size[1]/100))
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
    plt.axis('off')
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
    plt.close()

# Lista para armazenar as classificações e tempos
resultados = []

# Processar cada segmento de áudio
for i in range(41):  # Iterar sobre os 41 segmentos
    # Nome do arquivo do segmento
    segment_file = os.path.join(segmentos_dir, f'segment_{i*5}-{(i+1)*5}.mp3')
    espectrograma_file = os.path.join(output_dir, f'segment_{i*5}-{(i+1)*5}.png')
    
    # Converter o segmento em espectrograma
    audio_para_espectrograma(segment_file, espectrograma_file)
    
    # Carregar o espectrograma como imagem e preparar para o modelo
    img = load_img(espectrograma_file, target_size=(128, 128))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalizar a imagem

    # Fazer a previsão
    pred = model.predict(img_array)
    
    # Armazenar o resultado para cada emoção
    probabilidades_emocoes = pred.flatten().tolist()  # Obter a lista de probabilidades para as 28 emoções
    tempo_inicio = f"{(i*5)//60:02d}:{(i*5)%60:02d}"
    resultados.append([tempo_inicio] + probabilidades_emocoes)

# Nome das colunas (tempo inicial + 28 classes de emoção)
colunas = ['Trecho_Inicial'] + [f'Emocao_{j+1}' for j in range(28)]

# Criar a tabela com os tempos e probabilidades para cada emoção
df = pd.DataFrame(resultados, columns=colunas)

# Salvar em CSV
df.to_csv('classificacoes_musicaJACKSON.csv', index=False)
print("Tabela de classificações salva como 'classificacoes_musicaJACKSON.csv'")