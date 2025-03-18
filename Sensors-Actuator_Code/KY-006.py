from machine import Pin, PWM
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/actuador/ky006"

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

# Configurar buzzer
buzzer = PWM(Pin(16))  # GPIO18 para el buzzer
buzzer.freq(1000)  # Frecuencia del buzzer

try:
    while True:
        # Encender buzzer
        buzzer.duty(512)  # 50% ciclo de trabajo
        print("Buzzer encendido")
        client.publish(MQTT_TOPIC, "1")  # Publicar estado
        time.sleep(1)  

        # Apagar buzzer
        buzzer.duty(0)
        print("Buzzer apagado")
        client.publish(MQTT_TOPIC, "0")  # Publicar estado
        time.sleep(5)  # Esperar 10 segundos

except KeyboardInterrupt:
    print("Programa terminado")
    buzzer.deinit()  # Apagar PWM
    wifi.disconnect()  # Desconectar WiFi
    client.disconnect()  # Cerrar conexión MQTT