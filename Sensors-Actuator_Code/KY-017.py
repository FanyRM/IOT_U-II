import machine
import time
import network
from umqtt.simple import MQTTClient

# 🔹 Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/sensor/ky017"

# 🔹 Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("Conectado a WiFi!")

# 🔹 Conectar a MQTT
client = MQTTClient("ESP32", MQTT_BROKER)
client.connect()
print("Conectado a MQTT!")

# 🔹 Configuración del sensor KY-017
KY017_PIN = 14  # GPIO donde está conectado el sensor (ajustar según conexión)
sensor_ky017 = machine.Pin(KY017_PIN, machine.Pin.IN)

# 🔹 Bucle de lectura y envío de datos
while True:
    estado = sensor_ky017.value()  # Leer estado del sensor

    if estado == 0:
        mensaje = "Sensor inclinado"
    else:
        mensaje = "Sensor en posición normal"

    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje)

    time.sleep(2)  # Enviar datos cada 2 segundos
