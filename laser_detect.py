from gpiozero import LED, LightSensor
from time import sleep
from signal import pause

led = LED(2)
ldr = LightSensor(4)

interrupt = False
count = 0

while True:
    print("Besucher: ", count)
    while interrupt is False:
        if ldr.value < 0.1:
            led.on()
            count += 1
            interrupt = True
        else:
            led.off()
    while interrupt is True:
        if ldr.value > 0.1:
            led.off()
            interrupt = False

pause()
