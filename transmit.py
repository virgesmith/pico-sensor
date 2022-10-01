import time
import machine
import wifi
import ujson
import jwt
from hashlib import sha1
import urequests as requests
import binascii

from umqtt.simple import MQTTClient

from sensors import temperature
from utils import secrets, utc_time_str

vccon_url = "https://fw-dt-vccon.azurewebsites.net/incoming/"
# vccon_url = "http://192.168.178.61:8000/incoming/"
mqtt_broker = "azpi4"
topic = "iaq"

INTERVAL = 300 # seconds


def make_token(data: dict, secret: str) -> str:
  m = sha1()
  m.update(ujson.dumps(data).encode('utf-8'))
  h = m.digest().hex()
  return jwt.encode({"checksum": h}, secret)


def mqtt_connect():
  client = MQTTClient(machine.unique_id().hex(), mqtt_broker, keepalive=3600)
  client.connect()
  print(f'Connected to {mqtt_broker} MQTT Broker')
  return client


led = machine.Pin("LED", machine.Pin.OUT)
led.on()

creds = secrets()
secret = binascii.a2b_base64(creds["SIGNATURE_SECRET"])

wifi.connect()

client = mqtt_connect()

while True:
  led.on()
  payload = {"device": "pico-w", "id": machine.unique_id().hex(), "value": { "temperature": temperature() }, "timestamp": utc_time_str() }
  token = make_token(payload, creds["FW_VCCON_SIGNATURE_SECRET"])
  headers = {'x-fw-signature': token }

  try:
    response = requests.post(vccon_url, headers=headers, json=payload)
    response.close()
  except Exception as e:
    print(f"{e.__class__.__name__} {e}")

  token = jwt.encode(payload, secret, algorithm='HS256')

  client.publish(topic, token)

  led.off()
  time.sleep(INTERVAL)

