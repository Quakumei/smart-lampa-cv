import time
from multiprocessing import Pipe

from config.settings import PIN_BUTTON_L, PIN_BUTTON_R
from modules.button_control.Button import Button
from modules.button_control.ButtonActions import ButtonAction

# def button_handler(conn: Pipe, btn: Button, buttons: tuple[Button]):
#     status = btn.action()
#     match status:
#         case ButtonStatus.EB_PRESS:
#             print("Press")
#         case ButtonStatus.EB_HOLD:
#             print("Hold")
#         case ButtonStatus.EB_STEP:
#             print("Step")
#         case ButtonStatus.EB_RELEASE:
#             print("Release")
#         case ButtonStatus.EB_CLICK:
#             print("Click")
#         case ButtonStatus.EB_CLICKS:
#             print(f"Clicks: {btn.getClicks()} times")
#         case ButtonStatus.EB_REL_HOLD:
#             print("Release Hold")
#         case ButtonStatus.EB_REL_HOLD_C:
#             print("Release Hold C")
#         case ButtonStatus.EB_REL_STEP:
#             print("Release Step")
#         case ButtonStatus.EB_REL_STEP_C:
#             print(f"Release Step C with {btn.getClicks()} clicks")
#         case _:
#             pass
#     if btn.click():
#         conn.send({'pin': btn.pin, 'event': ButtonStatus.EB_CLICK})
#     if btn.hold():
#         conn.send({'pin': btn.pin, 'event': ButtonStatus.EB_HOLD})
#     if btn.step():
#         conn.send({'pin': btn.pin, 'event': ButtonStatus.EB_STEP})
#     if btn.holdWithClicks(1):
#         conn.send({'pin': btn.pin, 'event': ButtonStatus.EB_REL_HOLD_C,})
last_left_click_time = 0
last_right_click_time = 0


def button_handler(conn: Pipe, btn: Button, buttons: tuple[Button, Button], swipe_timeout=0.5):
    global last_left_click_time, last_right_click_time
    left_button, right_button = buttons

    # Determine which button (left or right) is being interacted with
    if btn == left_button:
        button_prefix = 'L_'
        last_click_time = last_left_click_time
    elif btn == right_button:
        button_prefix = 'R_'
        last_click_time = last_right_click_time
    else:
        return  # Unknown button

    current_time = time.time()

    # Check for specific button actions and send corresponding enum to the pipe
    if btn.click():
        conn.send(ButtonAction[button_prefix + 'CLICK'])

        # Check for swipe action
        if button_prefix == 'L_' and (current_time - last_right_click_time) <= swipe_timeout:
            conn.send(ButtonAction['R_SWIPE'])
        elif button_prefix == 'R_' and (current_time - last_left_click_time) <= swipe_timeout:
            conn.send(ButtonAction['L_SWIPE'])

        # Update last click time
        if button_prefix == 'L_':
            last_left_click_time = current_time
        elif button_prefix == 'R_':
            last_right_click_time = current_time

    elif btn.hold():
        conn.send(ButtonAction[button_prefix + 'HOLD'])
    elif btn.holdWithClicks(1):
        conn.send(ButtonAction[button_prefix + 'CLICK_HOLD'])
    elif btn.getClicks() == 2:
        conn.send(ButtonAction[button_prefix + 'DOUBLE_CLICK'])
    elif btn.step():
        conn.send(ButtonAction[button_prefix + 'STEP'])


def send_msg(conn, message):
    conn.send(message)


def run(conn):
    button_l = Button(PIN_BUTTON_L)
    button_r = Button(PIN_BUTTON_R)
    buttons = (button_l, button_r)
    button_l.attach(lambda: button_handler(conn, button_l, buttons))
    button_r.attach(lambda: button_handler(conn, button_r, buttons))
    print("Start")
    while True:
        button_l.tick()
        button_r.tick()


if __name__ == "__main__":
    run()
