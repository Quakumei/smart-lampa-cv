import multiprocessing

from modules.button_control import button_controller


def main():
    # camera_proc = multiprocessing.Process(target=hand_tracking_controller.run, args=())
    # movement_proc = multiprocessing.Process(target=movement_controller.run, args=())
    # led_proc = multiprocessing.Process(target=led_controller.run, args=())
    # button controller
    parent_button_action_conn, child_button_action_conn = multiprocessing.Pipe()
    button_proc = multiprocessing.Process(target=button_controller.run, args=(child_button_action_conn,))

    # camera_proc.start()
    # movement_proc.start()
    # led_proc.start()
    button_proc.start()

    while True:
        message = parent_button_action_conn.recv()
        print(f"Received message: {message}")


if __name__ == "__main__":
    main()
