import time
from machine import Pin
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/sensor/ky021"

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

# Configurar el pin digital donde está conectado el sensor KY-021
boton = Pin(34, Pin.IN, Pin.PULL_UP)  # El pin debe estar configurado como entrada con pull-up interno

while True:
    # Leer el estado del botón (LOW cuando está presionado)
    if not boton.value():
        print("Botón no presionado")
        estado_boton = "No presionado"
    else:
        print("Botón presionado")
        estado_boton = "Presionado"

    # Publicar el estado del botón en el tópico MQTT
    client.publish(MQTT_TOPIC, estado_boton)

    time.sleep(2)  # Espera de 2 segundos
