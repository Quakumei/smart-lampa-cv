from config.settings import PIN_BUTTON_L, PIN_BUTTON_R
from modules.button_control.Button import Button


def button_l_handler(a):
    print(f'handler {a}')


def demo():
    button_l = Button(PIN_BUTTON_L)
    button_r = Button(PIN_BUTTON_R)

    print("Start")
    while True:
        button_l.tick()
        button_r.tick()
        a, b = button_l.action(), button_r.action()
        if a or b:
            print(a, b)


if __name__ == "__main__":
    demo()
