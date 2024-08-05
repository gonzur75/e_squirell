import gc

import esp
import network

from config import PASSWORD, SSID
from helpers import check_connection
from helpers.helpers import restart_and_reconnect

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
        restart_and_reconnect(error)
