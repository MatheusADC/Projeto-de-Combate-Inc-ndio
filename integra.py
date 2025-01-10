#!/usr/bin/python3
import gpiod
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import urllib.parse
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import cv2
import numpy as np
import tensorflow as tf
import threading

# Configuração do MongoDB
client = MongoClient("mongodb+srv://YOUR_MONGODB_INFO.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["db"]
colection = db["wppAutomatize"]
document = colection.find_one({"_id": ObjectId("YOUR_OBJECT_ID")})

# Configuração do GPIO
chip = gpiod.Chip('gpiochip4')
line = chip.get_line(21)  # Sensor de chama
relay_line = chip.get_line(20)  # Relé da bomba de água
line.request(consumer='flame_sensor', type=gpiod.LINE_REQ_EV_BOTH_EDGES)
relay_line.request(consumer='water_pump', type=gpiod.LINE_REQ_DIR_OUT)

# Inicialização do Selenium
options = webdriver.ChromeOptions()
options.add_argument("YOUR_USER_DATA_PATH")
service = Service("YOUR_CHROMEDRIVER_PATH")

# Variável global para os nomes das classes
class_names = []

# Flag para controle de ativação da bomba
pump_active = False

def send_whatsapp_message(contatos, message):
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 100)

    for contato in contatos:
        # Codificar a mensagem para URL
        text = urllib.parse.quote(message)
        link = f"https://web.whatsapp.com/send?phone={contato['phone']}&text={text}"
        
        driver.get(link)
        time.sleep(5)  # Espera o link carregar

        # Aguardar o carregamento da caixa de mensagem
        message_box_path = '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]'
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_path)))
        message_box.send_keys(Keys.ENTER)
        
        time.sleep(5)  # Espera um pouco antes de enviar o próximo

        print(f"Mensagem enviada para: {contato['name']}")

def handle_flame_sensor():
    global pump_active  # Utiliza a flag para controle da bomba
    message_sent = False  # Flag para controlar o envio da mensagem

    while True:
        if line.event_wait(sec=10):
            value = line.get_value()
            print(f"Pinagem: {value}")

            if value == 0 and not pump_active:  # Chama detectada
                print("Chama detectada!")
                pump_active = True
                relay_line.set_value(1)  # Liga a bomba
                time.sleep(10)  # Liga a bomba por 10 segundos
                relay_line.set_value(0)  # Desliga a bomba após 10 segundos
                pump_active = False

                # Envia mensagem se não tiver sido enviada
                if not message_sent and document:
                    contatos = document["contatos"]
                    message = "Um incêndio foi detectado! Procure a saída de emergência mais próxima!"
                    send_whatsapp_message(contatos, message)
                    message_sent = True  # Marca que a mensagem foi enviada

            elif value == 1:  # Chama não detectada
                print("Chama não detectada!")
                message_sent = False  # Permite novo envio de mensagem

        else:
            print("Nenhum evento do sensor de chama")

def load_images_from_folder(folder):
    images = []
    labels = []
    global class_names
    class_names = os.listdir(folder)  # Lista das classes
    for label, class_name in enumerate(class_names):
        class_path = os.path.join(folder, class_name)
        if os.path.isdir(class_path):
            for filename in os.listdir(class_path):
                img_path = os.path.join(class_path, filename)
                img = cv2.imread(img_path)
                if img is not None:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converte para escala de cinza
                    img = cv2.resize(img, (64, 64))  # Redimensiona
                    img = np.expand_dims(img, axis=-1) / 255.0  # Normaliza e adiciona o canal
                    images.append(img)
                    label_array = np.zeros(len(class_names))
                    label_array[label] = 1
                    labels.append(label_array)
    return np.array(images), np.array(labels)

# Carrega o modelo
model_path = 'fire_detection_model.h5'
if os.path.exists(model_path):
    model = tf.keras.models.load_model(model_path)
    print("Modelo carregado com sucesso.")
else:
    print("Modelo não encontrado. Treine e salve o modelo primeiro.")
    exit()

# Certifique-se de que load_images_from_folder() é chamado antes de iniciar as threads
images, labels = load_images_from_folder('images')

def handle_image_detection():
    global pump_active
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow("Webcam", frame)

        k = cv2.waitKey(1)
        
        if k == 27:  # Pressione 'ESC' para sair
            break
        elif k == ord("p"):  # Pressione 'p' para tirar a foto e fazer a previsão
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized_frame = cv2.resize(gray_frame, (64, 64))
            normalized_frame = np.expand_dims(resized_frame, axis=-1) / 255.0
            sample_image = np.expand_dims(normalized_frame, axis=0)

            # Realiza a previsão
            predict = model.predict(sample_image)
            predicted_label = np.argmax(predict[0])  # Pega o índice da maior probabilidade
            confidence = np.max(predict[0])  # Pega a confiança da previsão
            
            if predicted_label < len(class_names) and class_names[predicted_label] == "incendio" and not pump_active:
                print("Incêndio detectado pela imagem!")
                pump_active = True
                relay_line.set_value(1)  # Liga a bomba
                time.sleep(10)  # Liga a bomba por 10 segundos
                relay_line.set_value(0)  # Desliga a bomba após 10 segundos
                pump_active = False

                if document:
                    contatos = document["contatos"]
                    message = "Um incêndio foi detectado! Procure a saída de emergência mais próxima!"
                    send_whatsapp_message(contatos, message)
            else:
                print("Sem detecção de incêndio.")

    cap.release()
    cv2.destroyAllWindows()

# Iniciar as threads
flame_thread = threading.Thread(target=handle_flame_sensor)
image_thread = threading.Thread(target=handle_image_detection)

flame_thread.start()
image_thread.start()

flame_thread.join()
image_thread.join()

# Finaliza o controle da bomba
relay_line.set_value(0)  # Garante que a bomba esteja desligada
relay_line.release()
