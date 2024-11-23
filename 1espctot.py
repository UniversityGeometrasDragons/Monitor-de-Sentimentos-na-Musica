import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

def gerar_espectrograma(arquivo_audio, salvar_em):
    try:
        # Carregar o áudio
        y, sr = librosa.load(arquivo_audio, sr=None)
        
        # Gerar o Mel-spectrograma
        S = librosa.feature.melspectrogram(y=y, sr=sr)
        S_db = librosa.power_to_db(S, ref=np.max)  # Converter para escala dB
        
        # Plotar o espectrograma e salvar como imagem
        plt.figure(figsize=(5, 5))
        librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='mel')
        plt.axis('off')  # Remove eixos
        plt.savefig(salvar_em, bbox_inches='tight', pad_inches=0)
        plt.close()
        
        print(f"Espectrograma salvo em: {salvar_em}")
    except Exception as e:
        print(f"Erro ao processar {arquivo_audio}: {e}")

# Caminho do áudio e da imagem de saída
#audio_file = "C:\base\Verified_Normed\_4IRMYuE1hI_160.mp3"
#output_image = "C:\base\espectrograma.png"

# Gerar espectrograma
#gerar_espectrograma(audio_file, output_image)


def processar_varios_audios(pasta_audio, pasta_saida):
    for arquivo in os.listdir(pasta_audio):
        if arquivo.endswith(".mp3"):
            caminho_audio = os.path.join(pasta_audio, arquivo)
            caminho_imagem = os.path.join(pasta_saida, f"{arquivo[:-4]}.png")
            gerar_espectrograma(caminho_audio, caminho_imagem)

# Exemplo de uso:
processar_varios_audios(r"C:\base\Verified_Normed", r"C:\base\EspecsTOT")