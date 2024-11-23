import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pydub import AudioSegment
from pydub.playback import play
import threading
from moviepy.editor import AudioFileClip, VideoFileClip

# Carregar as classificações
df = pd.read_csv('classificacoes_musicaSONATA.csv')
dados_emocoes = df.drop(columns=['Trecho_Inicial'], errors='ignore')

# Carregar o áudio
audio_path = r"C:\base\EXPERIMENTO4\Beethoven - Sonata ao Luar (Moonlight Sonata) [v2jir8opKlc].mp3"
audio = AudioSegment.from_mp3(audio_path)

# Verificar se os dados estão corretamente formatados
print(dados_emocoes.head())

# Configuração inicial para o gráfico
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(28)  # Cada índice representa uma emoção
bars = ax.bar(x, np.zeros(28), color="orange")  # Inicializar com barras de altura 0

# Configuração do gráfico
emocoes = dados_emocoes.columns.tolist()
ax.set_ylim(0, 1)
ax.set_xticks(x)
ax.set_xticklabels(emocoes, rotation=90)
ax.set_ylabel("Intensidade da Chama")
ax.set_title("Beethoven - Sonata ao Luar (Moonlight Sonata) = Evolução das Emoções ao Longo da Música em Barras")

# Adicionar texto para o tempo decorrido
tempo_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color="black", fontsize=12)
# Adicionar texto para a emoção predominante
emocao_predominante_text = ax.text(0.02, 0.90, '', transform=ax.transAxes, color="red", fontsize=12)

# Função de atualização para a animação
def update(frame):
    intensidades = dados_emocoes.iloc[frame]  # Intensidade para cada emoção no trecho atual
    for bar, intensidade in zip(bars, intensidades):
        bar.set_height(intensidade)  # Ajusta a altura conforme a intensidade
        bar.set_color(plt.cm.autumn(intensidade))  # Cor de chama

    # Identifica a emoção com a maior pontuação
    indice_max = np.argmax(intensidades)
    emocao_max = emocoes[indice_max]
    valor_max = intensidades[indice_max] * 100
    
    # Exibir a emoção predominante e sua intensidade
    emocao_predominante_text.set_text(f"Emoção predominante: {emocao_max} com {valor_max:.2f}%")

    # Atualizar o tempo decorrido na animação
    tempo_decorrido = frame * 5  # Em segundos, assumindo trechos de 5 segundos
    minutos = tempo_decorrido // 60
    segundos = tempo_decorrido % 60
    tempo_text.set_text(f"Tempo: {minutos:02d}:{segundos:02d}")

    return [*bars, tempo_text, emocao_predominante_text]

# Função para tocar o áudio
def tocar_audio():
    time.sleep(5)
    os.system(f'start vlc "{audio_path}"')

# Configurar a animação
frames = len(dados_emocoes)
ani = FuncAnimation(fig, update, frames=frames, blit=True, interval=5000)  # Intervalo de 5 segundos

# Salvar a animação como vídeo sem áudio
video_path = 'animation.mp4'
ani.save(video_path, writer='ffmpeg', fps=0.2)  # Ajuste de fps para 1 para manter os intervalos de 5 segundos

# Carregar o arquivo de áudio
audio_clip = AudioFileClip(audio_path)

# Carregar o vídeo salvo
video_clip = VideoFileClip(video_path)

# Ajustar a duração do vídeo para o áudio (se necessário)
video_clip = video_clip.set_duration(audio_clip.duration)

# Definir o áudio no vídeo
video_with_audio = video_clip.set_audio(audio_clip)

# Salvar o vídeo final com áudio
final_video_path = 'final_videoSONATA.mp4'
video_with_audio.write_videofile(final_video_path, codec='libx264', fps=1)  # Ajuste de fps para 1

# Iniciar a reprodução de áudio em uma thread separada
thread_audio = threading.Thread(target=tocar_audio)
thread_audio.start()

# Exibir a animação
plt.show()

# Esperar a thread de áudio terminar
thread_audio.join()