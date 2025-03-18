from machine import Pin
import time
import network
from umqtt.simple import MQTTClient
import ir_rx  # Esta librería es para leer las señales IR

# Configuración de WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"  # Dirección IP de tu broker MQTT (Mosquitto)
MQTT_TOPIC = "cerm/sensor/ky022"  # Tema para publicar los datos del sensor IR

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

# Configuración del pin del receptor IR (KY-022)
pin_ir = Pin(34, Pin.IN)  # Utilizamos el GPIO34 para leer la señal IR

# Crear una instancia del receptor IR
ir_sensor = ir_rx.IRReceiver(pin_ir)

# Función para manejar la señal IR cuando se recibe un dato
def on_ir_receive(data):
    print("Dato IR recibido: ", data)  # Imprime el dato IR
    client.publish(MQTT_TOPIC, str(data))  # Publica el dato recibido en MQTT

# Configurar el receptor IR para escuchar señales
ir_sensor.callback(on_ir_receive)

while True:
    time.sleep(1)  # Mantener el loop activo para recibir señales IR
