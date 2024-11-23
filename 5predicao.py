from tensorflow.keras.models import load_model
import numpy as np
import tensorflow as tf

# Carregar o modelo treinado
model = load_model("modelo_emocoesEUA.h5")

# Função para carregar espectrograma de 5 segundos
def carregar_espectrograma_5s(arquivo_audio):
    # Aqui você deve gerar um espectrograma para o intervalo de 5s do áudio
    img_path = f"EspecsTOT/{arquivo_audio.replace('.mp3', '.png')}"
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(128, 128))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)  # Ajustar o formato

# Exemplo de predição para uma nova música
novo_espectrograma = carregar_espectrograma_5s("4YxTa1AUqps_26.mp3")
predicao = model.predict(novo_espectrograma)

# Exibir resultados
# Defina as emoções de acordo com as saídas do modelo
emocoes = ["Amusing","Angry","Annoying","Anxious","Awe-inspiring","Beautiful","Bittersweet","Calm","Compassionate","Dreamy","Eerie","Energizing","Entrancing","Erotic","Euphoric","Exciting","Goose bumps","Indignant","Joyful","Nauseating","Painful","Proud","Romantic","Sad","Scary","Tender","Transcendent","Triumphant"
]  # Ajuste conforme necessário

# Imprime todas as emoções previstas
for i, valor in enumerate(predicao[0]):
    if i < len(emocoes):
        print(f"{emocoes[i]}: {valor * 100:.2f}%")
    else:
        print(f"Emoção extra prevista: {valor * 100:.2f}%")

# Identifica a emoção com a maior pontuação
indice_max = np.argmax(predicao[0])
emocao_max = emocoes[indice_max]
valor_max = predicao[0][indice_max] * 100

print(f"\nEmoção predominante: {emocao_max} com {valor_max:.2f}%")