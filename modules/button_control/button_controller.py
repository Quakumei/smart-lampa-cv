# git clone –recursive https://github.com/orangepi-xunlong/wiringOP-Python -b next
import time
from modules.button_control.Button import Button

PIN_BUTTON_L = 4
PIN_BUTTON_R = 5

button_l = Button(PIN_BUTTON_L)
button_r = Button(PIN_BUTTON_R)
'''
for i in range(0, 100):
    wiringpi.pinMode(i, wiringpi.GPIO.INPUT)
    print(i, wiringpi.digitalRead(i))
    time.sleep(0.2)
    
'''    
print("Start")
while True:
    button_l.tick()
    button_r.tick()
    a, b = button_l.action(), button_r.action()
    if a or b:
        print(a, b)
