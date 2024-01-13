# git clone –recursive https://github.com/orangepi-xunlong/wiringOP-Python -b next
from config.settings import PIN_BUTTON_L, PIN_BUTTON_R
from modules.button_control.Button import Button


def run():
    button_l = Button(PIN_BUTTON_L)
    button_r = Button(PIN_BUTTON_R)
    while True:
        button_l.tick()
        button_r.tick()
