import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split

print("TensorFlow version:", tf.__version__)

# Defina as dimensões desejadas para as imagens
width, height = 64, 64  

# Função para carregar imagens e rótulos do banco de imagens
def load_images_from_folder(folder):
    images = []
    labels = []
    # Lista das classes
    class_names = os.listdir(folder)  
    for label, class_name in enumerate(class_names):
        class_path = os.path.join(folder, class_name)
        if os.path.isdir(class_path):
            for filename in os.listdir(class_path):
                img_path = os.path.join(class_path, filename)
                img = cv2.imread(img_path)
                if img is not None:
                    # Converte para escala de cinza
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
                     # Redimensionamento das imagens
                    img = cv2.resize(img, (width, height)) 
                    # Normaliza e adiciona o canal
                    img = np.expand_dims(img, axis=-1) / 255.0  
                    images.append(img)
                    label_array = np.zeros(len(class_names))
                    label_array[label] = 1
                    labels.append(label_array)
    return np.array(images), np.array(labels), class_names

# Carrega as imagens e rótulos do banco de imagens
images, y, class_names = load_images_from_folder('images')

# Divide o conjunto de dados em treino e validação
train_images, val_images, train_labels, val_labels = train_test_split(images, y, test_size=0.2, random_state=42)

# Verifica o número de classes e ajusta a camada de saída do modelo
num_classes = len(class_names)

# Definição do modelo com camadas convolucionais - neurônios
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(height, width, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    # Adiciona Dropout (remoção/abandono dos neurônios que não estão sendo usados, juntamente com as suas conexões) para evitar overfitting ("engesamento" da rede neural em que ela não consegue prever a resposta correta para situações que não foram "vistas" na fase de treinamento)
    tf.keras.layers.Dropout(0.25),  
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    # Mais Dropout
    tf.keras.layers.Dropout(0.5),  
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer=tf.optimizers.Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Caminho para salvar o modelo treinado
model_path = 'fire_detection_model.h5'

# Verifique se o modelo já foi treinado e salvo
if os.path.exists(model_path):
    # Carregar o modelo treinado
    model = tf.keras.models.load_model(model_path)
    print("Modelo carregado com sucesso.")
else:
    # Data augmentation (técnica pra maximizar a qualidade dos dados, melhorando o desempenho do modelo)
    train_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    val_datagen = ImageDataGenerator()  # Sem aumento de dados para a validação

    # Treinamento do modelo (as épocas são como se fossem gerações para o treinamento ou para os testes)
    EPOCHS = 1000 
    # O batch_size é o número de exemplos (imagens) que serão usadas em uma iteração (1 EPOCH)
    train_generator = train_datagen.flow(train_images, train_labels, batch_size=16) 
    val_generator = val_datagen.flow(val_images, val_labels, batch_size=16)
    
    model.fit(train_generator, epochs=EPOCHS, validation_data=val_generator)

    # Salvar o modelo treinado
    model.save(model_path)
    print("Modelo treinado e salvo com sucesso!")

# Captura de imagem pela webcam para fazer previsões
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("Webcam", frame)

    k = cv2.waitKey(1)
    
    # Pressione 'ESC' para sair
    if k == 27:  
        break
    # Pressione 'p' para tirar a foto e fazer a previsão
    elif k == ord("p"):  
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray_frame, (width, height))
        normalized_frame = np.expand_dims(resized_frame, axis=-1) / 255.0
        sample_image = np.expand_dims(normalized_frame, axis=0)
        
        # Realiza a previsão
        predict = model.predict(sample_image)
        # Pega o índice da maior probabilidade
        predicted_label = np.argmax(predict[0])  
        # Pega a confiança da previsão
        confidence = np.max(predict[0])  
        print("Predict Label:", class_names[predicted_label])
        print("Confidence:", confidence)
        print("Predict:", predict)

cap.release()
cv2.destroyAllWindows()
