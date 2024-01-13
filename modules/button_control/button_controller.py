from config.settings import PIN_BUTTON_L, PIN_BUTTON_R
from modules.button_control.Button import Button
from modules.button_control.ButtonStatus import ButtonStatus


def button_handler(btn: Button, a):
    status = btn.action()
    print(f'Handler {a} get {status}')
    match status:
        case ButtonStatus.EB_PRESS:
            print("Press")
        case ButtonStatus.EB_HOLD:
            print("Hold")
        case ButtonStatus.EB_STEP:
            print("Step")
        case ButtonStatus.EB_RELEASE:
            print("Release")
        case ButtonStatus.EB_CLICK:
            print("Click")
        case ButtonStatus.EB_CLICKS:
            print(f"Clicks: {btn.getClicks()} times")
        case ButtonStatus.EB_REL_HOLD:
            print("Release Hold")
        case ButtonStatus.EB_REL_HOLD_C:
            print("Release Hold C")
        case ButtonStatus.EB_REL_STEP:
            print("Release Step")
        case ButtonStatus.EB_REL_STEP_C:
            print("Release Step C")
        case _:
            print("Unknown status")


def demo():
    button_l = Button(PIN_BUTTON_L)
    button_r = Button(PIN_BUTTON_R)
    button_l.attach(button_handler(button_l, 0))
    button_r.attach(button_handler(button_r, 1))
    print("Start")
    while True:
        button_l.tick()
        button_r.tick()
        a, b = button_l.action(), button_r.action()
        if a or b:
            print(a, b)


if __name__ == "__main__":
    demo()
