import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración del sensor
PHOTO_SENSOR_PIN = 18
sensor = machine.Pin(PHOTO_SENSOR_PIN, machine.Pin.IN)

# Configuración de la red WiFi
WIFI_SSID = 'celeste'
WIFI_PASSWORD = '12345678'

# Configuración del broker MQTT
MQTT_BROKER = '192.168.137.191'  # Ejemplo: '192.168.1.10'
MQTT_PORT = 1883
MQTT_TOPIC = 'cerm/sensor/ky010'

# Función para conectar el ESP32 a WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print('Conectado a WiFi')

# Conectar al WiFi
connect_wifi()

# Función para publicar mensajes en el broker MQTT
def mqtt_callback(topic, msg):
    print('Mensaje recibido:', topic, msg)

# Crear el cliente MQTT
client = MQTTClient('ESP32_client', MQTT_BROKER, port=MQTT_PORT)
client.set_callback(mqtt_callback)
client.connect()

# Publicar el estado del fototransistor
try:
    while True:
        # Leer el estado del fototransistor
        if sensor.value() == 1:
            print("Luz detectada")
            client.publish(MQTT_TOPIC, "Luz detectada")
        else:
            print("Sin luz")
            client.publish(MQTT_TOPIC, "Sin luz")
        
        # Esperar 1 segundo antes de la siguiente lectura
        time.sleep(3)

except KeyboardInterrupt:
    print("Programa detenido por el usuario")
    client.disconnect()