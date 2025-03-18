from machine import Pin
import time

# Definir los pines a los que están conectados los LEDs
led_pins = [14, 12, 13, 15, 16, 17, 18, 19, 21, 22, 2, 4, 23, 5]  # Cambia estos números si usas otros pines

# Configurar los pines de los LEDs como salida
leds = [Pin(pin, Pin.OUT) for pin in led_pins]

# Función para encender todos los LEDs al mismo tiempo
def encender_leds():
    for led in leds:
        led.on()  # Enciende el LED

# Función para apagar todos los LEDs al mismo tiempo
def apagar_leds():
    for led in leds:
        led.off()  # Apaga el LED

# Bucle principal
while True:
    encender_leds()  # Enciende todos los LEDs
    time.sleep(1)    # Mantiene los LEDs encendidos por 1 segundo
    apagar_leds()    # Apaga todos los LEDs
    time.sleep(1)    # Mantiene los LEDs apagados por 1 segundo
