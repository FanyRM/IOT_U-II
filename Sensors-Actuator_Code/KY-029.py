from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración de WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"  # Dirección IP de tu broker MQTT (Mosquitto)
MQTT_TOPIC = "cerm/actuador/ky029"  # Tema para publicar el color del LED

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

# Configuración de los pines para los LED de dos colores
led_rojo = Pin(23, Pin.OUT)  # Pin para el LED rojo
led_verde = Pin(22, Pin.OUT)  # Pin para el LED verde

while True:
    # Encender el LED rojo y apagar el verde
    led_rojo.value(1)
    led_verde.value(0)
    print("rojo")
    client.publish(MQTT_TOPIC, "rojo")  # Publicar el color en MQTT
    time.sleep(3)

    # Encender el LED verde y apagar el rojo
    led_rojo.value(0)
    led_verde.value(1)
    print("verde")
    client.publish(MQTT_TOPIC, "verde")  # Publicar el color en MQTT
    time.sleep(3)

