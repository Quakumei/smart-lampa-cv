# git clone –recursive https://github.com/orangepi-xunlong/wiringOP-Python -b next
import wiringpi
from wiringpi import GPIO

PIN_BUTTON_L = 2
PIN_BUTTON_R = 3


class ButtonController:
    def __init__(self, pin_l, pin_r):
        wiringpi.wiringPiSetup()

        wiringpi.pinMode(PIN_BUTTON_L, GPIO.INPUT)
        wiringpi.pinMode(PIN_BUTTON_R, GPIO.INPUT)
        wiringpi.wiringPiISR(pin_l, 2, self.interrupt_button_l)
        wiringpi.wiringPiISR(pin_r, 2, self.interrupt_button_r)

    def interrupt_button_l(self):
        pass

    def interrupt_button_r(self):
        pass
