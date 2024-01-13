from config.settings import PIN_BUTTON_L, PIN_BUTTON_R
from modules.button_control.Button import Button


def button_handler(btn, a):
    print(f'handler {a} get {btn.action()}')


def demo():
    button_l = Button(PIN_BUTTON_L)
    button_r = Button(PIN_BUTTON_R)
    button_l.attach(lambda: button_handler(button_l, "a"))
    button_r.attach(lambda: button_handler(button_r, "b"))

    print("Start")
    while True:
        button_l.tick()
        button_r.tick()

demo()
