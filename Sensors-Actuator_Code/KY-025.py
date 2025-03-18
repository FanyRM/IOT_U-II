from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/sensor/ky025"

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

# Configuración del pin digital del sensor KY-025 (por ejemplo, GPIO14)
sensor_ky025 = Pin(34, Pin.IN)  # Pin GPIO14 para la lectura digital

while True:
    valor_digital = sensor_ky025.value()  # Leer el valor digital del sensor

    print(f"Valor digital del sensor KY-025: {valor_digital}")
    
    # Publica el valor digital en MQTT
    client.publish(MQTT_TOPIC, str(valor_digital))

    time.sleep(3)  # Esperar 5 segundos antes de la siguiente lectura
