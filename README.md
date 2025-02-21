# <img src="https://github.com/user-attachments/assets/caabfdf0-0f9e-44a3-8200-c6579fe87887" alt="ícone de descrição" width="28"> Descrição
O projeto tem como objetivo desenvolver um dispositivo inteligente para a detecção de chamas, integrando diferentes tecnologias para maior eficiência e precisão. O sistema utiliza um sensor infravermelho (IR) para a detecção física das chamas, complementado por uma webcam conectada a uma rede neural convolucional capaz de identificar visualmente imagens de incêndios. Além de enviar alertas pelo WhatsApp para os números cadastrados, o dispositivo é capaz de acionar automaticamente uma bomba de água, ampliando sua funcionalidade em situações de emergência.

# <sub><img src="https://img.icons8.com/?size=100&id=13443&format=png&color=000000" alt="ícone raspberry" width="35"></sub>Requisitos
 - Raspberry Pi 5 Model B Anatel - 4GB 
 - Mini Bomba D’água Submersiva 3-6V
 - Módulo Relé 5V 1 Canal
 - Protoboard - 400 furos
 - Kit Jumpers 20cm x120 Unidades
 - Sensor de Chama Fogo 760 a 1100 nm
 - Case Raspberry Pi 5 Oficial
 - Cabo Micro HDMI 1,50 Metros
 - Cartão de Memória 64GB MicroSd Kingston Classe 10 com Adaptador

# <img src="https://github.com/user-attachments/assets/7f4c8b3e-5b48-406b-b71a-cf9e3b4dae76" alt="ícone de simulação" width="28"> Simulação Virtual
![image](https://github.com/user-attachments/assets/ec15b02d-56f0-45f2-ab42-6bb226c082a8)

<br>

> [!CAUTION]
> É importante destacar que a imagem acima do protótipo apresentado não reflete fielmente o resultado final, representando apenas uma das possíveis configurações. Isso se deve à dificuldade de encontrar simuladores gratuitos que ofereçam, de forma gráfica, suporte ao Raspberry Pi 5 e a outros componentes eletroeletrônicos.

<br>

# <img src="https://github.com/user-attachments/assets/50dcad50-441e-4743-a494-a895c859a26b" alt="ícone de circuito" width="38"> Montagem do circuito
### Pinout da Raspberry Pi 5
![image](https://github.com/user-attachments/assets/267423cd-4968-404b-a3ab-0c3b1d964dd5)
<br>

1. Conecte uma extremidade do jumper no pino 2(5V) e a outra extremidade na porção positiva da protoboard;
2. Conecte uma extremidade do jumper no pino 6(0V) e a outra extremidade na porção negativa da protoboard;
3. Conecte uma extremidade do jumper no pino 38(GPIO 20) e a outra extremidade no pino S do relé;
4. Conecte uma extremidade do jumper no pino + do relé e a outra extremidade na porção positiva da protoboard;
5. Conecte uma extremidade do jumper no pino - do relé e a outra extremidade na porção negativa da protoboard;
6. Conecte uma extremidade do jumper no pino 40(GPIO 21) e a outra extremidade no pino D0 do sensor IR;
7. Conecte uma extremidade do jumper no pino GND do sensor IR e a outra extremidade na porção negativa da protoboard;
8. Conecte uma extremidade do jumper no pino VCC do sensor IR e a outra extremidade na porção positiva da protoboard;
9. Conecte uma extremidade do jumper na porta NO do relé e a outra extremidade positiva(fio vermelho) da minibomba de água;
10. Conecte uma extremidade do jumper na porta COM do relé e a outra extremidade na porção positiva da protoboard;
11. Conecte uma extremidade do jumper na extremidade negativa(fio preto) da minibomba de água e a outra extremidade na porção negativa da protoboard;

## Instalação da biblioteca gpiod pelo shell do Linux
```
sudo apt-get install -y gpiod
```
## Instalação da biblioteca gpiod pelo gerenciador de pacotes do python
```
pip install gpiod
```
## Verificação da instalação da biblioteca gpiod
```
gpiodetect
```
## Verificação da porta ligada ao pino 21 (flame sensor)
```
gpioinfo
```
## Executar programa no terminal
```
sudo python3 main.py
```
<br>

> [!CAUTION]
> O interpretador do python deve estar no diretório /usr/bin/python3

<br>

## Instalação da biblioteca OpenCV
```
sudo apt install python3-opencv
```
## Instalação da biblioteca numpy
```
sudo apt install python3-numpy
```
<br>

> [!CAUTION]
> Para o projeto foi obrigatório utilizar a versão 1.0 (deprecada) do numpy. Para realizar o downgrade:
> 
> **pip3 install "numpy<2"**

<br>

## Preparação para instalação do TensorFlow
```
sudo apt install libatlas-base-dev
```

## Instalação da biblioteca TensorFlow
```
pip3 install tensorflow --break-system-packages
```

## Instalação da biblioteca sklearn
```
pip3 install scikit-learn --break-system-packages
```

## Verificação da detecção da webcam 
```
lsusb
```

## Instalação do Selenium
```
pip3 install selenium --break-system-packages
```

## Instalação da biblioteca PyMongo
```
pip3 install pymongo --break-system-packages
```

## Novas funcionalidades
Com o objetivo de assistir pessoas com deficiência visual e auditiva, pode-se implementar o uso de um Módulo Buzzer Ativo(5V) e de LEDs, respectivamente.

# <img src="https://github.com/user-attachments/assets/1a4f98ce-8de0-41af-96fc-42b9ba49a7d0" alt="ícone de placa" width="30"> Prototipação
### Imagem 1
![image](https://github.com/user-attachments/assets/b8417b9a-54ac-41f3-98a2-28c40aee54c2)

<p>

### Imagem 2
![image](https://github.com/user-attachments/assets/a6436af1-76c1-4280-8580-7d29a66a887f)

