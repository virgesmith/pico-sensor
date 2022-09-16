import time
import machine
import network
import ujson
import jwt
from hashlib import sha1
import urequests as requests

vccon_url = "https://fw-dt-vccon.azurewebsites.net/incoming/"
# vccon_url = "http://192.168.178.61:8000/incoming/"

INTERVAL = 300 # seconds

with open("secrets.json","r") as fh:
  creds = ujson.load(fh)


def utc_time_str() -> str:
  """e.g. 2022-09-07T10:00:00Z"""
  OFFSET = 3600 # gmtime=localtime
  (y, m, d, h, min, s, _, _) = time.gmtime(time.time() - OFFSET)
  return f"{y:04d}-{m:02d}-{d:02d}T{h:02d}:{min:02d}:{s:02d}Z"


SENSOR_TEMP = machine.ADC(4)
CONVERSION_FACTOR = 3.3 / (65535)


def temperature():
  reading = SENSOR_TEMP.read_u16() * CONVERSION_FACTOR
  return 27 - (reading - 0.706) / 0.001721


def make_token(data: dict, secret: str) -> str:
  m = sha1()
  m.update(ujson.dumps(data).encode('utf-8'))
  h = m.digest().hex()
  return jwt.encode({"checksum": h}, secret)

led = machine.Pin("LED", machine.Pin.OUT)
led.on()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(creds["WIFI_SSID"], creds["WIFI_PASS"])

# TODO set time from ntp

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

while True:
  led.on()
  # TODO add timestamp...
  payload = {"device": "pico-w", "id": machine.unique_id().hex(), "value": { "temperature": temperature() }}
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

