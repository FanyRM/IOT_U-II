from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient

# Configuración de WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"  # Dirección IP de tu broker MQTT (Mosquitto)
MQTT_TOPIC = "cerm/sensor/ky024"  # Tópico para publicar los datos del sensor

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

# Configuración del pin digital (presencia de campo magnético)
pin_digital = Pin(34, Pin.IN)  # Pin GPIO34 para la señal digital (detecta presencia de imán)

# Configuración del pin analógico (intensidad del campo magnético)
pin_analogico = ADC(Pin(35))  # Pin GPIO35 para leer la intensidad del campo magnético

# Ajuste de rango para las lecturas analógicas (0-1023)
pin_analogico.atten(ADC.ATTN_0DB)

while True:
    # Leer el valor digital (1 si hay campo magnético, 0 si no)
    valor_digital = pin_digital.value()

    # Leer el valor analógico (intensidad del campo magnético)
    valor_analogico = pin_analogico.read()

    # Crear un diccionario con los datos del sensor
    data = {
        "Campo Magnético Detectado": "Sí" if valor_digital == 1 else "No",
        "Intensidad del Campo Magnético": valor_analogico
    }

    # Convertir el diccionario a JSON
    json_data = str(data)

    # Publicar los datos en el tópico MQTT
    client.publish(MQTT_TOPIC, json_data)

    # Imprimir los valores por consola
    print(f"Publicado: {json_data}")

    time.sleep(1)  # Espera 1 segundo antes de la siguiente lectura
