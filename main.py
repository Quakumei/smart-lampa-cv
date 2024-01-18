import multiprocessing

from main_controller import controller
from modules.button_control import button_controller
from modules.led_control import led_controller


def main():
    # camera_proc = multiprocessing.Process(target=hand_tracking_controller.run, args=())
    # camera_proc.start()
    # movement_proc = multiprocessing.Process(target=movement_controller.run, args=())
    # movement_proc.start()
    # led controller
    parent_led_action_conn, child_led_action_conn = multiprocessing.Pipe(duplex=False)
    led_c = led_controller.LedController(parent_led_action_conn)
    led_proc = multiprocessing.Process(target=led_c.run)
    led_proc.start()
    # button controller
    parent_button_action_conn, child_button_action_conn = multiprocessing.Pipe(duplex=False)
    button_proc = multiprocessing.Process(target=button_controller.run, args=(child_button_action_conn,))
    print("Start button process starting...")
    button_proc.start()
    # main controller
    my_controller = controller.MainController(parent_button_action_conn, parent_led_action_conn)
    main_proc = multiprocessing.Process(target=my_controller.run)
    print("Main process starting...")
    main_proc.start()

    button_proc.join()
    main_proc.join()
    print("Finish")


if __name__ == "__main__":
    main()
