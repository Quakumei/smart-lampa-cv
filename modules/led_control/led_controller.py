import spidev
from PIL import ImageColor

import ws2812
from config.settings import LED_NUM

# Initialize SPI device
spi = spidev.SpiDev()
spi.open(0, 0)


def fill(led_sequence):
    """
    Fills the LED strip with a sequence of RGB colors.

    Args:
    led_sequence (list): A list of RGB tuples, each representing the color for an LED.

    Raises:
    ValueError: If the length of led_sequence does not match the expected LED_NUM.
    """
    # Check if the length of the input sequence matches the number of LEDs
    if len(led_sequence) != LED_NUM:
        raise ValueError(f"An array of size {LED_NUM} was expected, an array of size {len(led_sequence)} was received.")

    # Send the color data to the LED strip
    ws2812.write2812(spi, led_sequence)


def fill_hex_color(hex_color: str):
    """
    Fills the LED strip with a single color specified in hexadecimal format.

    Args:
    hex_color (str): The color in hexadecimal format (e.g., "#FF5733").
    """
    # Convert hex color to RGB tuple
    color = ImageColor.getcolor(hex_color, "RGB")

    # Fill the LED strip with the converted RGB color
    fill_color(*color)


def fill_color(R: int, G: int, B: int):
    """
    Fills the LED strip with a single RGB color.

    Args:
    R (int): Red component of the color (0-255).
    G (int): Green component of the color (0-255).
    B (int): Blue component of the color (0-255).
    """
    # Create a color data sequence for the entire strip
    data = [[G, R, B]] * LED_NUM

    # Send the color data to the LED strip
    ws2812.write2812(spi, data)


def turn_off():
    """
    Turns off all LEDs on the strip.
    """
    # Send an off command to all LEDs
    ws2812.off_leds(spi, LED_NUM)
