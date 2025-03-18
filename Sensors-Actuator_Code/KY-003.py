from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/sensor/ky003"

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


sensor_hall = Pin(33, Pin.IN)  # Conectar la salida del KY-003 al GPIO18

while True:
    estado = sensor_hall.value()  # Leer el estado del sensor

    if estado == 0:
        print("¡Campo magnético detectado!")
        client.publish(MQTT_TOPIC, str(estado))
        
    else:
        print("No hay campo magnético")
        client.publish(MQTT_TOPIC, str(estado))

    time.sleep(5)  # Esperar 0.5 segundos antes de la siguiente lectura