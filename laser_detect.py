from gpiozero import LED, LightSensor
from time import sleep
from signal import pause

led = LED(2)
ldr = LightSensor(4)

while True:
    ldr.when_dark = led.on()
    ldr.when_light = led.off()

pause()
