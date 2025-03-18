import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# Configuración Wi-Fi
WIFI_SSID = "celeste"
WIFI_PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.191"
MQTT_PORT = 1883
MQTT_TOPIC = "cerm/sensor/ky027"
MQTT_CLIENT_ID = "sensor_{}".format(int(time.time()))

# Pines del sensor y LED
shock_sensor = Pin(2, Pin.IN, Pin.PULL_UP)
led = Pin(15, Pin.OUT)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    for _ in range(10):
        if wlan.isconnected():
            print('Conectado a Wi-Fi:', wlan.ifconfig())
            return True
        time.sleep(1)
    print("Error: No se pudo conectar a Wi-Fi")
    return False

def connect_mqtt():
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar MQTT:", e)
        return None

def publish_sensor_state(client, last_state):
    if not client:
        print("MQTT no conectado")
        return last_state
    try:
        estado = "1" if shock_sensor.value() == 0 else "0"
        if estado != last_state:
            client.publish(MQTT_TOPIC, estado)
            print("Estado enviado:", estado)
            led.value(int(estado))
        return estado
    except Exception as e:
        print("Error en sensor:", e)
        return last_state

if connect_wifi():
    client = connect_mqtt()
    last_state = None
    while True:
        last_state = publish_sensor_state(client, last_state)
        time.sleep(0.5)
else:
    print("Reinicia el dispositivo.")