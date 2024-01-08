import numpy as np
from PIL import Image

import led_control

# LED matrix layout
LED_MATRIX = np.array([
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
], dtype=np.uint8)

def process_image(image_path):
    """
    Process an image: crop it to a square and resize to 10x10 pixels.
    :param image_path: Path to the image file.
    :return: 10x10 numpy array representing the processed image.
    """
    # Open the image
    with Image.open(image_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Crop the image to a square
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = (width + min_dim) // 2
        bottom = (height + min_dim) // 2
        img_cropped = img.crop((left, top, right, bottom))

        # Resize the image to 10x10 pixels
        img_resized = img_cropped.resize((10, 10), Image.LANCZOS)

        # Convert to numpy array
        img_array = np.array(img_resized)[..., [1, 0, 2]]  # convert RGB to GRB that used by ws2812

        return img_array


def convert_image_to_led_matrix(image, led_matrix=LED_MATRIX):
    """
    Convert a 10x10 image to a sequence for an LED strip with a specific layout
    :param image: A 10x10 numpy array representing the image.
    :param led_matrix: A 10x10 numpy array representing the LED matrix layout (1 for LED, 0 for hole).
    :return: Numpy array representing the LED sequence.
    """
    # Initialize an array to hold the LED data
    led_data = []

    # Iterate through each row in the LED matrix
    for row_index in range(10):
        # Extract the corresponding row from the image and the LED matrix
        image_row = image[row_index]
        led_row = led_matrix[row_index]

        # Filter the row data based on the LED matrix
        row_data = image_row[led_row == 1]

        # Reverse the row data for even rows (0-indexed)
        if row_index % 2 == 1:
            row_data = row_data[::-1]
        # Append the row data to the LED data array
        led_data.extend(row_data)
    return np.array(led_data)
