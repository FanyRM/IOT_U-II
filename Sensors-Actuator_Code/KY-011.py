import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "celeste"
PASSWORD = "12345678"
MQTT_BROKER = "192.168.137.191"
MQTT_TOPIC = "cerm/actuador/ky011"

# Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)
print("Conectado a WiFi:", wifi.ifconfig())

# Conectar a MQTT
client = MQTTClient("ESP32_KY011", MQTT_BROKER)
client.connect()
print("Conectado a MQTT!")

# Configuración del actuador:
# Asumimos que el actuador se controla a través de un único pin (por ejemplo, el pin 13).
# Si el actuador requiere control de intensidad, se puede usar PWM.
actuador_pin = machine.Pin(4, machine.Pin.OUT)
# Si se requiere PWM, descomenta la siguiente línea:
# pwm_actuador = machine.PWM(actuador_pin, freq=1000)

# Ejemplo de bucle para encender y apagar el actuador
while True:
    # Encender el actuador (o establecer un duty mayor si usas PWM)
    actuador_pin.on()
    mensaje = "Actuador encendido"
    client.publish(MQTT_TOPIC, mensaje.encode())
    print(mensaje)
    time.sleep(3)
    
    # Apagar el actuador (o establecer un duty menor si usas PWM)
    actuador_pin.off()
    mensaje = "Actuador apagado"
    client.publish(MQTT_TOPIC, mensaje.encode())
    print(mensaje)
    time.sleep(3)
