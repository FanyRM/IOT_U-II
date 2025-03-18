import dht
import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/sensor/ky015"


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



dht_pin = machine.Pin(4)
sensor = dht.DHT11(dht_pin)

while True:
    try:
        sensor.measure()
        temperatura = sensor.temperature()
        humedad = sensor.humidity()
        
        mensaje = f"{temperatura}.{humedad}"
        
        client.publish(MQTT_TOPIC, mensaje)
        print(f"Temperatura: {temperatura}°C, Humedad: {humedad}%")
    except OSError as e:
        print("Error al leer el sensor", e)
    time.sleep(1)