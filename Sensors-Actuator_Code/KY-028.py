import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/sensor/ky028"

# Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("Conectado a WiFi!")

# Conectar a MQTT
client = MQTTClient("ESP32_KY028", MQTT_BROKER)
client.connect()
print("Conectado a MQTT!")

# Configuración del sensor KY-028
ky028_digital = machine.Pin(4, machine.Pin.IN)  # DO conectado al GPIO4
ky028_analog = machine.ADC(machine.Pin(35))  # AO conectado al GPIO36 (VP en ESP32)
ky028_analog.atten(machine.ADC.ATTN_11DB)  # Rango completo (0 - 3.3V)

# Bucle principal para enviar datos
while True:
    # Leer salida digital (DO)
    estado = ky028_digital.value()  # 1 = temperatura alta, 0 = normal
    estado_texto = "Alto" if estado == 1 else "Bajo"
    
    # Leer salida analógica (AO)
    temperatura_raw = ky028_analog.read()  # Valor entre 0 y 4095
    temperatura_volt = (temperatura_raw / 4095) * 3.3  # Convertir a voltios

    # Publicar en MQTT
    mensaje = f"Estado Digital: {estado_texto}, Temperatura Analógica: {temperatura_volt:.2f}V"
    client.publish(MQTT_TOPIC, mensaje.encode())

    print(mensaje)

    time.sleep(2)  # Espera 2 segundos antes de la siguiente lectura
