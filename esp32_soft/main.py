from mqtt import restart_and_reconnect


def run():
    try:
        CLIENT.check_msg()
    except OSError as e:
        restart_and_reconnect(e)
    return


while True:
    run()
