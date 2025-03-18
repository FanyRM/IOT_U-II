from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración de WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"  # Dirección IP de tu broker MQTT (Mosquitto)
MQTT_TOPIC = "cerm/actuador/ky040"  # Tema para publicar los pulsos del encoder

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

# Configuración del pin del encoder KY-040
pin_encoder = Pin(34, Pin.IN, Pin.PULL_UP)  # Conectamos el pin de señal al GPIO14

# Variable para contar los pulsos del encoder
pulsos = 0

# Función de interrupción para contar los pulsos del encoder
def contar_pulsos(pin):
    global pulsos
    pulsos += 1  # Incrementa el contador de pulsos cada vez que se detecta un cambio

# Configurar la interrupción para detectar los pulsos del encoder
pin_encoder.irq(trigger=Pin.IRQ_RISING, handler=contar_pulsos)  # Interrupción en flanco ascendente

while True:
    # Publicar el valor de pulsos cada 1 segundo
    client.publish(MQTT_TOPIC, str(pulsos))  # Publica el número de pulsos en MQTT
    print(f"Valor de pulsos: {pulsos}")
    
    time.sleep(3)  # Espera 1 segundo antes de publicar el siguiente valor
