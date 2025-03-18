from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración de WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"  # Dirección IP de tu broker MQTT (Mosquitto)
MQTT_TOPIC = "cerm/sensor/ky036"  # Tema para publicar el estado del sensor táctil

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

# Configuración del pin de salida digital del sensor KY-036
sensor_ky036 = Pin(23, Pin.IN)  # Asume que el pin de salida DO está conectado al pin GPIO23

while True:
    # Leer el estado digital del sensor (HIGH o LOW)
    estado_sensor = sensor_ky036.value()

    # Si el valor del sensor es 1, significa que el sensor está tocado o se ha detectado un objeto conductor
    if estado_sensor == 1:
        print("Sensor tocado o objeto conductor detectado.")
        client.publish(MQTT_TOPIC, "tocado")  # Publica el estado en MQTT
    else:
        print("Sensor no tocado.")
        client.publish(MQTT_TOPIC, "no_tocado")  # Publica el estado en MQTT
    
    time.sleep(1)  # Esperar 1 segundo antes de la siguiente lectura
