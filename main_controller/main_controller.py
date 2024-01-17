# consume work
from modules.button_control.ButtonActions import ButtonAction
from modules.button_control.ButtonStatus import ButtonStatus


def run(button_conn):
    print('Receiver: Running', flush=True)
    # consume work
    while True:
        # get a unit of work
        item = button_conn.recv()
        # report
        print(f'>receiver got {ButtonAction(item)}', flush=True)
