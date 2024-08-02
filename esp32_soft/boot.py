import gc

import esp

from config import PASSWORD, SSID
from helpers import wlan_connect
from helpers.helpers import restart_and_reconnect

esp.osdebug(0)
gc.collect()

try:
    wlan_connect(SSID, PASSWORD)
except OSError as error:
    restart_and_reconnect(error)


