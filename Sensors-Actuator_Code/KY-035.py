from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración de WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"  # Dirección IP de tu broker MQTT (Mosquitto)
MQTT_TOPIC = "cerm/sensor/ky035"  # Tema para publicar el estado del sensor

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

# Configuración del pin de salida digital del sensor KY-035
sensor_ky035 = Pin(23, Pin.IN)  # Asume que el pin de salida DO está conectado al pin GPIO23

while True:
    # Leer el estado digital del sensor (HIGH o LOW)
    estado_sensor = sensor_ky035.value()

    # Si el valor del sensor es 1, significa que hay un campo magnético cercano
    if estado_sensor == 1:
        print("Campo magnético detectado.")
        client.publish(MQTT_TOPIC, "campo_magnetico")  # Publica el estado en MQTT
    else:
        print("No se detecta campo magnético.")
        client.publish(MQTT_TOPIC, "sin_campo")  # Publica el estado en MQTT
    
    time.sleep(1)  # Esperar 1 segundo antes de la siguiente lectura
