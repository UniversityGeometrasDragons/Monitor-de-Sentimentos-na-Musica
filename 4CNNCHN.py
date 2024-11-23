import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
import numpy as np

# 1. Carregar os dados do CSV
csv_path = "musicas_emocoesCHN.csv"
dados = pd.read_csv(csv_path)

# 2. Separar nomes dos arquivos e rótulos
arquivos = dados["Arquivo MP3"].values
rotulos = dados.drop("Arquivo MP3", axis=1).values  # Remove a coluna com os nomes

# 3. Função para carregar os espectrogramas como arrays de imagem
def carregar_espectrograma(nome):
    img_path = f"EspecsTOT/{nome.replace('.mp3', '.png')}"
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(128, 128))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0  # Normalizar
    return img_array

# 4. Carregar todas as imagens e rótulos em arrays
imagens = np.array([carregar_espectrograma(nome) for nome in arquivos])
rotulos = np.array(rotulos)  # Rótulos já estão carregados do CSV

# 5. Definir o modelo CNN
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(rotulos.shape[1], activation='sigmoid')  # Multi-label
])

# 6. Compilar o modelo
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# 7. Treinar o modelo
model.fit(imagens, rotulos, epochs=80, batch_size=32, validation_split=0.2)

# 8. Salvar o modelo treinado
model.save("modelo_emocoesCHN.h5")
print("Modelo salvo como 'modelo_emocoesCHN.h5'.")