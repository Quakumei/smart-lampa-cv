# git clone –recursive https://github.com/orangepi-xunlong/wiringOP-Python -b next

from modules.button_control.Button import Button

PIN_BUTTON_L = 2
PIN_BUTTON_R = 3

button_l = Button(PIN_BUTTON_L)
button_r = Button(PIN_BUTTON_R)

while True:
    button_l.tick()
    button_r.tick()
