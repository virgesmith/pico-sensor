import time
import machine
import network
import ujson
import jwt
from hashlib import sha1
import urequests as requests

vccon_url = "https://fw-dt-vccon.azurewebsites.net/incoming/"

with open("secrets.json","r") as fh:
  creds = ujson.load(fh)

def make_token(data, secret):
  m = sha1()
  sorted_data = dict(sorted(data.items(), key=lambda item: item[0]))
  m.update(ujson.dumps(sorted_data).encode('utf-8'))
  h = m.digest().hex()
  print(h)
  return jwt.encode({"checksum": h}, secret)

led = machine.Pin("LED", machine.Pin.OUT)
led.on()

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

while True:
  led.on()
  payload = {"device": "pico-w", "id": machine.unique_id().hex(), "value": { "temperature": 10.0 }, "timestamp": time.time()}
  token = make_token(payload, creds["FW_VCCON_SIGNATURE_SECRET"])
  print(token)
  headers = {'x-fw-signature': token} #'accept': 'application/json', 'Content-Type': 'application/json' }

  try:
    print("sending...")
    response = requests.post(vccon_url, headers=headers, data=ujson.dumps(payload))
    print("sent (" + str(response.status_code) + "), status = " + str(wlan.status()) )
    response.close()
  except Exception as e:
    print(f"{e} could not connect (status =" + str(wlan.status()) + ")")
    if wlan.status() < 0 or wlan.status() >= 3:
      print("trying to reconnect...")
      wlan.disconnect()
      wlan.connect(ssid, password)
      if wlan.status() == 3:
        print('connected')
      else:
        print('failed')
  led.off()
  time.sleep(15)

