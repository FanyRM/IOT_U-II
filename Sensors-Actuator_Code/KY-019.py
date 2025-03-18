import time
from machine import Pin
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/actuador/ky019"

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

# Conectar el actuador al pin GPIO23
actuador_pin = Pin(23, Pin.OUT)  # Definir el pin donde está conectado el relay

while True:
    # Encender el relay
    actuador_pin.value(1)
    print("Relay encendido")
    client.publish(MQTT_TOPIC, "Encendido")
    time.sleep(2)  # Esperar 2 segundos
    
    # Apagar el relay
    actuador_pin.value(0)
    print("Relay apagado")
    client.publish(MQTT_TOPIC, "Apagado")
    time.sleep(2)  # Esperar 2 segundos
