import random
import time
from machine import Pin, ADC
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/sensor/ky013"


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


# Conectar el sensor al pin GPIO34
sensor_pin = Pin(34)  # Definir el pin donde está conectado el sensor
sensor = ADC(sensor_pin)  # Configurar el pin como ADC (analógico)

# Configurar el rango de lectura (por defecto es de 0 a 4095)
sensor.atten(ADC.ATTN_0DB)  # Establecer atenuación de 0dB para leer voltajes de 0-3.3V

while True:
    valor = sensor.read()  # Leer el valor analógico
    print('Valor del sensor:', valor)  # Imprimir el valor en la consola de Thonny
    
    client.publish(MQTT_TOPIC, str(valor))
    time.sleep(2)  # Esperar 1 segundo antes de la siguiente lectura