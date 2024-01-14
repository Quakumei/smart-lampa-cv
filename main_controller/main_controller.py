# consume work
def run(button_conn):
    print('Receiver: Running', flush=True)
    # consume work
    while True:
        # get a unit of work
        item = button_conn.recv()
        # report
        print(f'>receiver got {item}', flush=True)
        # check for stop
        if item is None:
            break
    # all done
    print('Receiver: Done', flush=True)
