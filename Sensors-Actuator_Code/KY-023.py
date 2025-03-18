from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient
import ujson  # Librería para trabajar con JSON en MicroPython

# Configuración de WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"  # Dirección IP de tu broker MQTT (Mosquitto)
MQTT_TOPIC = "cerm/sensor/ky023"  # Tópico para publicar los datos del joystick

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

# Configuración de los pines analógicos del joystick
pin_joystick_x = ADC(Pin(34))  # Pin GPIO34 para el eje X
pin_joystick_y = ADC(Pin(35))  # Pin GPIO35 para el eje Y

# Configuración del pin digital para el botón del joystick
pin_button = Pin(32, Pin.IN, Pin.PULL_UP)  # Pin GPIO32 para el botón (con pull-up interno)

# Ajuste de rango para las lecturas analógicas (0-1023)
pin_joystick_x.atten(ADC.ATTN_0DB)
pin_joystick_y.atten(ADC.ATTN_0DB)

while True:
    # Leer el valor analógico de los ejes X e Y
    valor_x = pin_joystick_x.read()
    valor_y = pin_joystick_y.read()

    # Leer el estado del botón (LOW si está presionado, HIGH si no lo está)
    button_state = "Presionado" if pin_button.value() == 0 else "No presionado"

    # Crear un diccionario con todos los datos
    data = {
        "X": valor_x,
        "Y": valor_y,
        "Boton": button_state
    }

    # Convertir el diccionario a JSON
    json_data = ujson.dumps(data)

    # Publicar todos los valores en el mismo tópico en formato JSON
    client.publish(MQTT_TOPIC, json_data)

    # Imprimir los valores por consola
    print(f"Publicado: {json_data}")

    time.sleep(1)  # Espera 1 segundo antes de la siguiente lectura
