import time
import ntptime
import machine
import rp2
import network
import ujson
import jwt
from hashlib import sha1
import urequests as requests

from sensors import temperature
from utils import secrets, utc_time_str

vccon_url = "https://fw-dt-vccon.azurewebsites.net/incoming/"
# vccon_url = "http://192.168.178.61:8000/incoming/"

INTERVAL = 300 # seconds


def make_token(data: dict, secret: str) -> str:
  m = sha1()
  m.update(ujson.dumps(data).encode('utf-8'))
  h = m.digest().hex()
  return jwt.encode({"checksum": h}, secret)

led = machine.Pin("LED", machine.Pin.OUT)
led.on()

creds = secrets()

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
else:
  print('connected')
  status = wlan.ifconfig()
  print( 'ip = ' + status[0] )

led.off()

# set time from ntp
ntptime.settime()

while True:
  led.on()
  # TODO add timestamp...
  payload = {"device": "pico-w", "id": machine.unique_id().hex(), "value": { "temperature": temperature() }, "timestamp": utc_time_str() }
  token = make_token(payload, creds["FW_VCCON_SIGNATURE_SECRET"])
  headers = {'x-fw-signature': token }

  try:
    # print(f"sending {ujson.dumps(payload)}")
    response = requests.post(vccon_url, headers=headers, json=payload)
    # print("sent (" + str(response.status_code) + "), status = " + str(wlan.status()) )
    response.close()
  except Exception as e:
    print(f"{e.__class__.__name__} {e} (WLAN status={wlan.status()})")
  led.off()
  time.sleep(INTERVAL)

