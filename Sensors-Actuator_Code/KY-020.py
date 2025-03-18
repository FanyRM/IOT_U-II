import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/sensor/ky020"

# Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("Conectado a WiFi!")

# Conectar a MQTT
client = MQTTClient("ESP32_KY020", MQTT_BROKER)
client.connect()
print("Conectado a MQTT!")

# Configuración del sensor KY-020
ky020_pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)  # GPIO4 con resistencia pull-up

while True:
    try:
        estado = ky020_pin.value()  # Leer el estado del sensor
        mensaje = "INCLINADO" if estado == 0 else "NORMAL"

        client.publish(MQTT_TOPIC, mensaje.encode())
        print(f"Estado del sensor KY-020: {mensaje}")
    except OSError as e:
        print("Error al leer el sensor", e)
    
    time.sleep(3)  # Espera 1 segundo antes de la siguiente lectura
