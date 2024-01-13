import wiringpi
from wiringpi import GPIO

from modules.button_control.VirtualButton import VirtualButton
wiringpi.wiringPiSetup()

class Button(VirtualButton):
    def __init__(self, npin=0, mode=GPIO.INPUT, btnLevel=GPIO.LOW):
        super().__init__()
        self.pin = npin
        wiringpi.pinMode(self.pin, mode)
        self.setBtnLevel(btnLevel == GPIO.LOW)

    def read(self):
        """ Read the current value of the button (without debounce). """
        return wiringpi.digitalRead(self.pin) ^ self._read_bf(self.EB_INV)

    def tick(self, **kwargs):
        """ Process the button, call in the main loop.
            TIPS: Make it async later
        Args:
            **kwargs:
        """
        return super().tick(wiringpi.digitalRead(self.pin))

    def tickRaw(self, **kwargs):
        """ Process the button without resetting events and without calling callback.

        Args:
            **kwargs:
        """
        return super().tickRaw(wiringpi.digitalRead(self.pin))

