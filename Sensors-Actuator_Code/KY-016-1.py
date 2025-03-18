import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/actuador/ky016"

# Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("Conectado a WiFi!")

# Conectar a MQTT
client = MQTTClient("ESP32_KY016", MQTT_BROKER)
client.connect()
print("Conectado a MQTT!")

# Configuración de pines para KY-016 (usando PWM)
pin_red = machine.Pin(13, machine.Pin.OUT)
pin_green = machine.Pin(12, machine.Pin.OUT)
pin_blue = machine.Pin(14, machine.Pin.OUT)

pwm_red = machine.PWM(pin_red, freq=1000)
pwm_green = machine.PWM(pin_green, freq=1000)
pwm_blue = machine.PWM(pin_blue, freq=1000)

# Definir colores (R, G, B)
colors = [
    (255, 255, 255, "Blanco"),      # Rojo
    (0, 255, 0, "Rojo"),     # Verde
    (0, 0, 255, "Azul"),      # Azul
    (255, 255, 0, "Amarillo"), # Amarillo
    (255, 0, 255, "Cian"), # Magenta
    (0, 255, 255, "Magenta"),    # Cian
    (255, 0, 0, "Verde"),
    (0, 0, 0, "Apagado")      # Apagado
]

# Función para cambiar el color del LED
def set_color(r, g, b):
    pwm_red.duty(int(r * 1023 / 255))  # Convierte 0-255 a 0-1023
    pwm_green.duty(int(g * 1023 / 255))
    pwm_blue.duty(int(b * 1023 / 255))

# Bucle principal para cambiar colores automáticamente
while True:
    for r, g, b, color_name in colors:
        set_color(r, g, b)
        
        # Publicar el color actual en MQTT
        mensaje = f"{color_name}"
        client.publish(MQTT_TOPIC, mensaje.encode())
        
        print(mensaje)
        
        time.sleep(3)  # Espera 3 segundos antes de cambiar al siguiente color
