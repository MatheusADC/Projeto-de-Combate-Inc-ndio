# Projeto de Combate ao Incêndio
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
