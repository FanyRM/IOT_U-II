from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración de WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"  # Dirección IP de tu broker MQTT (Mosquitto)
MQTT_TOPIC = "cerm/actuador/ky034"  # Tema para publicar el color del LED

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

# Configuración de los pines para el LED de 7 colores (KY-034)
pin_control = Pin(23, Pin.OUT)  # Asigna el pin adecuado para el control del LED

def encender_color(color):
    """
    Cambia el estado del pin de control del LED para encender el color deseado.
    El color se pasa como una cadena de texto.
    """
    if color == "rojo":
        pin_control.value(1)  # Enciende el LED rojo
    elif color == "verde":
        pin_control.value(2)  # Enciende el LED verde
    elif color == "azul":
        pin_control.value(3)  # Enciende el LED azul
    elif color == "amarillo":
        pin_control.value(4)  # Enciende el LED amarillo
    elif color == "morado":
        pin_control.value(5)  # Enciende el LED morado
    elif color == "cian":
        pin_control.value(6)  # Enciende el LED cian
    elif color == "blanco":
        pin_control.value(7)  # Enciende el LED blanco
    else:
        print(f"Color {color} no reconocido.")
        pin_control.value(0)  # Apaga el LED si el color no es válido

while True:
    # Ejemplo de ciclo para enviar diferentes colores
    colores = ["rojo", "verde", "azul", "amarillo", "morado", "cian", "blanco"]
    
    for color in colores:
        encender_color(color)  # Cambiar el color del LED
        print(f"{color} encendido")
        client.publish(MQTT_TOPIC, color)  # Publicar el color en MQTT
        time.sleep(3)  # Esperar 3 segundos antes de cambiar el color
