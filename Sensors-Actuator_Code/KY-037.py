import network
import time
import machine
from umqtt.simple import MQTTClient

SSID = "celeste"
PASSWORD = "12345678"

MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/sensor/ky037"

sensor_sonido = machine.ADC(machine.Pin(34))
sensor_sonido.atten(machine.ADC.ATTN_11DB)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("Conectado a WiFi!")

client = MQTTClient("ESP32", MQTT_BROKER)
client.connect()
print("Conectado a MQTT!")

while True:
    lectura = sensor_sonido.read()
    voltaje = lectura * (3.3 / 4095)
    mensaje = f"Ruido: {lectura}, Voltaje: {voltaje:.2f}V"
    mensajeF = str(lectura)

    print(f"Enviando: {mensaje}")
    client.publish(MQTT_TOPIC, mensajeF)

    time.sleep(1)