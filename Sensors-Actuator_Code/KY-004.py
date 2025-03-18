from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/actuador/ky004"


# Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("Conectado a WiFi!")

# Conectar a MQTT
client = MQTTClient("ESP32", MQTT_BROKER)
client.connect()
print("Conectado a MQTT!")


BOTON_PIN = 4  # GPIO donde conectaste el KY-004

boton = Pin(BOTON_PIN, Pin.IN, Pin.PULL_UP)  # Configurar el pin como entrada con resistencia pull-up

while True:
    if boton.value() == 0:  # El botón está presionado (LOW)
        print("¡Botón presionado!")
    else:
        print("Botón liberado")
    
    client.publish(MQTT_TOPIC, str(boton.value()))
    time.sleep(3)  # Pequeño retraso para evitar lecturas erróneas