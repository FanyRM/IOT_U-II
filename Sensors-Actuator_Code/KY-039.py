from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient

# Configuración de WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"  # Dirección IP de tu broker MQTT (Mosquitto)
MQTT_TOPIC = "cerm/sensor/ky039"  # Tema para publicar el pulso

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

# Configuración del pin analógico del sensor KY-039 (A0)
sensor_ky039_analog = ADC(Pin(34))  # Pin GPIO34 para la lectura analógica

# Configuración del rango de lectura analógica (0-1023)
sensor_ky039_analog.atten(ADC.ATTN_0DB)  # Ajuste de rango 0-1023

# Variables para el cálculo de la frecuencia cardíaca
tiempo_anterior = time.ticks_ms()
pulso = 0
num_pulsos = 0

while True:
    # Leer el valor analógico del sensor
    valor_analogico = sensor_ky039_analog.read()
    
    # Aquí normalmente tendrías que procesar la señal para detectar los picos del pulso
    # Pero por ahora simplemente contaremos las variaciones significativas
    if valor_analogico > 600:  # Umbral para detectar el pulso (ajustar según necesidad)
        num_pulsos += 1
        print("Pulso detectado!")
    
    # Calcular la frecuencia cardíaca cada 10 segundos
    if time.ticks_diff(time.ticks_ms(), tiempo_anterior) > 10000:  # Cada 10 segundos
        frecuencia_cardiaca = num_pulsos * 6  # Frecuencia en pulsos por minuto (bpm)
        print(f"Frecuencia cardíaca: {frecuencia_cardiaca} bpm")
        client.publish(MQTT_TOPIC, str(frecuencia_cardiaca))  # Publicar la frecuencia en MQTT
        # Restablecer los contadores para el siguiente cálculo
        num_pulsos = 0
        tiempo_anterior = time.ticks_ms()

    time.sleep(2)  # Esperar un poco antes de la siguiente lectura
