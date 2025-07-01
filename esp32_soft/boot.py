import gc

import esp
import network
import webrepl

from config import PASSWORD, SSID, WEBREPL_PASSWORD
from helpers import check_connection
from helpers import log_and_restart


esp.osdebug(None)
gc.collect()

print(f'Connecting to network: {SSID}.')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    try:
        wlan.connect(SSID, PASSWORD)
        check_connection(wlan)
    except OSError as error:
        log_and_restart(error)

webrepl.start(password=WEBREPL_PASSWORD)