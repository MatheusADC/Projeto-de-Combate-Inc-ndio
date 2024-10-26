from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import urllib.parse
from pymongo import MongoClient
from bson.objectid import ObjectId

# Conexão com o MongoDB
client = MongoClient('mongodb+srv://wppAutomatize:<<senhaAqui>>@cluster0.idvq4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client["db"]
colection = db["wppAutomatize"]

# Buscar o documento no MongoDB
document = colection.find_one({"_id": ObjectId("67155bdc24e4973449641009")})

# Configurações do Selenium
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/jlsam/AppData/Local/Google/Chrome/User Data")
service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://web.whatsapp.com/")

if document:
    contatos = document["contatos"]
    
    for contato in contatos:
        wait = WebDriverWait(driver, 100)
        message = "Oi, {}! {}".format(contato['name'], "tá pegando fogo, bicho!")
        
        # Codificar a mensagem para URL
        text = urllib.parse.quote(message)
        link = f"https://web.whatsapp.com/send?phone={contato['phone']}&text={text}"
        
        driver.get(link)
        time.sleep(5)
        
        # Aguardar o carregamento da caixa de mensagem
        message_box_path = '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]'
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_path)))
        message_box.send_keys(Keys.ENTER)
        
        time.sleep(5)  # Espera um pouco antes de enviar o próximo

        # Imprimir informações do contato
        print(f"Contato:")
        print(f"  Nome: {contato['name']}")
        print(f"  Telefone: {contato['phone']}")

# Fechar o navegador após o uso
driver.quit()