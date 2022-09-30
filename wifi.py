import network
import ujson
import rp2
import machine
import ntptime
import time
from utils import utc_time_str

from utils import secrets

def connect():

  creds = secrets()

  led = machine.Pin("LED", machine.Pin.OUT)
  led.on()

  rp2.country("GB")
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(creds["WIFI_SSID"], creds["WIFI_PASS"])

  # Wait for connect or fail
  max_wait = 10
  while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
      break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

  # Handle connection error
  if wlan.status() != 3:
    raise RuntimeError('network connection failed')

  # set time from ntp
  ntptime.settime()
  ip = wlan.ifconfig()[0]
  print(f'{utc_time_str()} connected, IP: {ip}')

  led.off()


