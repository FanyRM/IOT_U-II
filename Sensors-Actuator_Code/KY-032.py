from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/sensor/ky032"

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

# Configuración del pin digital del sensor KY-032 (por ejemplo, GPIO12)
sensor_ky032 = Pin(34, Pin.IN)  # Pin GPIO12 para la lectura digital

while True:
    valor_digital = sensor_ky032.value()  # Leer el valor digital del sensor

    if valor_digital == 1:
        print("¡Movimiento detectado!")
    else:
        print("No se detecta movimiento.")

    # Publica el valor digital en MQTT
    client.publish(MQTT_TOPIC, str(valor_digital))

    time.sleep(1)  # Esperar 1 segundo antes de la siguiente lectura
