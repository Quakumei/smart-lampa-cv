import multiprocessing

from main_controller import main_controller
from modules.button_control import button_controller


def main():
    # camera_proc = multiprocessing.Process(target=hand_tracking_controller.run, args=())
    # camera_proc.start()
    # movement_proc = multiprocessing.Process(target=movement_controller.run, args=())
    # movement_proc.start()
    # led_proc = multiprocessing.Process(target=led_controller.run, args=())
    # led_proc.start()
    # button controller
    parent_button_action_conn, child_button_action_conn = multiprocessing.Pipe(duplex=False)
    button_proc = multiprocessing.Process(target=button_controller.run, args=(child_button_action_conn,))
    print("Start button process starting...")
    button_proc.start()
    # main controller
    main_proc = multiprocessing.Process(target=main_controller.run, args=(parent_button_action_conn,))
    print("Main process starting...")
    main_proc.start()

    button_proc.join()
    main_proc.join()
    print("Finish")


if __name__ == "__main__":
    main()
