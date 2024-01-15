# Import the necessary libraries
from modules.button_control.VirtualButton import VirtualButton

wiringpi_available = False
try:
    # Try to import wiringpi
    import wiringpi

    wiringpi.wiringPiSetup()
    wiringpi_available = True

except ImportError:
    # Import keyboard as a fallback
    import keyboard


class Button(VirtualButton):
    def __init__(self, npin=0):
        super().__init__()
        self.pin = npin
        if wiringpi_available:
            wiringpi.pinMode(self.pin, wiringpi.INPUT)
            self.btnLevel = wiringpi.LOW

    def read(self):
        """
        Read the current value of the button (without debounce).
        DEBUG: If wiringpi not available, then use keyboard keys named like a pin of a button.
        """
        if wiringpi_available:
            return wiringpi.digitalRead(self.pin) ^ self._read_bf(self.EB_INV)
        else:
            return keyboard.is_pressed(chr(ord('0') - 4 + self.pin))

    def tick(self, **kwargs):
        """ Process the button, call in the main loop.
            TODO: Make it async later
        Args:
            **kwargs:
        """
        return super().tick(self.read())

    def tickRaw(self, **kwargs):
        """ Process the button without resetting events and without calling callback.
            TODO: Make it async later
        Args:
            **kwargs:
        """
        return super().tickRaw(self.read())

    # Define the Button class using keyboard library
    class Button(VirtualButton):
        def __init__(self, key):
            super().__init__()
            self.key = chr(ord('o') - 4 + key)

        def read(self):
            """ Read the current value of the button (mapped to a key). """
            return keyboard.is_pressed(self.key)

        def tick(self, **kwargs):
            """ Process the button, call in the main loop.
                TODO: Make it async later
            Args:
                **kwargs:
            """
            super().tick()

        def tickRaw(self):
            """ Process the button without resetting events and without calling callback. """
            # No additional logic for keyboard
            pass

    wiringpi_available = False


print(wiringpi_available)
