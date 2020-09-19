from gpiozero import LED, LightSensor
from time import sleep
from signal import pause

led = LED(2)
ldr = LightSensor(4)

print(ldr.value)
led.blink()

pause()
