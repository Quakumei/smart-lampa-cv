# Placeholder for the image path (to be replaced with the actual image path)
from modules.led_control import led_controller
from modules.led_control.image import process_image, convert_image_to_led_matrix


def test_image(image_path):
    # Process the image
    processed_image = process_image(image_path)

    # Convert the processed image to LED sequence
    led_sequence = convert_image_to_led_matrix(processed_image)
    # The led_sequence is now ready to be used with the ws2812.write2812 function
    led_controller.fill(led_sequence)


if __name__ == "__main__":
    test_image('/home/user/Downloads/Telegram Desktop/thumb.png')  # replace with the actual image path when available
