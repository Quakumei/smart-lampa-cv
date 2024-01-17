import time
from multiprocessing import Pipe

from config.settings import PIN_BUTTON_L, PIN_BUTTON_R, SWIPE_TIMEOUT
from modules.button_control.Button import Button
from modules.button_control.ButtonActions import ButtonAction
from modules.button_control.ButtonStatus import ButtonStatus

last_click_time = 0
last_click_prefix = None
flags_swipe = [False, False]


def get_state(btn: Button, buttons: tuple):
    global last_click_time, last_click_prefix, flags_swipe
    left_button, right_button = buttons

    # Determine which button (left or right) is being interacted with
    prefixes = ['L_', 'R_']
    if btn == left_button:
        button_prefix = 0
    elif btn == right_button:
        button_prefix = 1
    else:
        return  # Unknown button

    current_time = time.time()
    status = btn.action()
    res = None
    match status:
        # case ButtonStatus.EB_PRESS:
        #     print("Press")
        case ButtonStatus.EB_HOLD:
            # print("Hold")
            return ButtonAction.L_HOLD.value+button_prefix
        # case ButtonStatus.EB_STEP:
        #     print("Step")
        # case ButtonStatus.EB_RELEASE:
        #     print("Release")
        case ButtonStatus.EB_CLICK:
            if (current_time - last_click_time) <= SWIPE_TIMEOUT:
                if last_click_prefix == 0 and button_prefix == 1:
                    # print("R_SWIPE")
                    flags_swipe = [True, True]
                    res = ButtonAction.R_SWIPE.value
                elif last_click_prefix == 1 and button_prefix == 0:
                    # print("L_SWIPE")
                    flags_swipe = [True, True]
                    res = ButtonAction.L_SWIPE.value
            last_click_time = current_time
            last_click_prefix = button_prefix

        case ButtonStatus.EB_CLICKS:
            # print(f"Clicks: {btn.getClicks()} times")
            clicks = btn.getClicks()
            if not flags_swipe[button_prefix]:
                match clicks:
                    case 1:
                        # print(f"{prefixes[button_prefix]}CLICK")
                        res = ButtonAction.L_CLICK.value + button_prefix
                    case 2:
                        # print(f"{prefixes[button_prefix]}DOUBLE_CLICK")
                        res = ButtonAction.L_DOUBLE_CLICK.value + button_prefix
            flags_swipe[button_prefix] = False

        # case ButtonStatus.EB_REL_HOLD:
        #     print("Release Hold")
        # case ButtonStatus.EB_REL_HOLD_C:
        #     print("Release Hold C")
        case ButtonStatus.EB_REL_STEP:
            # print("Release Step")
            res = ButtonAction.L_REL_HOLD.value + button_prefix
        # case ButtonStatus.EB_REL_STEP_C:
        #     print(f"Release Step C with {btn.getClicks()} clicks")
        case _:
            pass
    return res


def button_handler(conn: Pipe, btn: Button, buttons: tuple[Button, Button]):
    state = get_state(btn, buttons)
    if state is not None:
        conn.send(state)


def run(conn):
    print("Button controller: Running", flush=True)
    button_l = Button(PIN_BUTTON_L)
    button_r = Button(PIN_BUTTON_R)
    buttons = (button_l, button_r)
    button_l.attach(lambda: button_handler(conn, button_l, buttons))
    button_r.attach(lambda: button_handler(conn, button_r, buttons))
    while True:
        button_l.tick()
        button_r.tick()
