# consume work
from multiprocessing.connection import Connection

from main_controller.LampMode import LampMode
from modules.button_control.ButtonActions import ButtonAction


# Main controller process
class MainController:
    def __init__(self, b_pipe: Connection, l_pipe: Connection):
        self.button_reactions = None
        self.button_pipe = b_pipe
        self.led_pipe = l_pipe
        self.current_mode = LampMode.LIGHT_TEMPERATURE
        self.setup_reactions()

    def setup_reactions(self):
        self.button_reactions = {
            ButtonAction.L_CLICK: self.toggle_mode_backward,
            ButtonAction.R_CLICK: self.toggle_mode_forward,
            ButtonAction.L_HOLD: self.start_brightness_up,
            ButtonAction.R_HOLD: self.start_brightness_down,
            ButtonAction.L_REL_HOLD: self.stop_change,
            ButtonAction.R_REL_HOLD: self.stop_change,
            ButtonAction.L_CLICK_HOLD: self.start_intensity_up,
            ButtonAction.R_CLICK_HOLD: self.start_intensity_down,
            ButtonAction.L_SWIPE: self.swipe_function,
            ButtonAction.R_SWIPE: self.swipe_function
        }

    def toggle_mode_forward(self):
        self.current_mode = LampMode((self.current_mode.value % len(LampMode)) + 1)
        print(f"mode {self.current_mode}")

    def toggle_mode_backward(self):
        value = self.current_mode.value - 1
        if value < 1:
            value = len(LampMode)
        self.current_mode = LampMode(value)
        print(f"mode {self.current_mode}")

    def start_brightness_up(self):
        # Logic to start changing brightness
        pass

    def start_brightness_down(self):
        # Logic to start changing brightness
        pass

    def stop_change(self):
        # Logic to stop changing anything
        pass

    def start_intensity_up(self):
        # Logic to start changing intensity/color temperature
        pass

    def start_intensity_down(self):
        # Logic to start changing intensity/color temperature
        pass

    def swipe_function(self):
        # Placeholder for swipe function
        pass

    def run(self):
        print('Main Controller: Running', flush=True)
        while True:
            if self.button_pipe.poll():
                action = ButtonAction(self.button_pipe.recv())
                print(f'>Main Controller got {action}', flush=True)
                if action in self.button_reactions:
                    self.button_reactions[action]()
