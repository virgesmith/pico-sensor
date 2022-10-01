import machine
import time
# import ujson
import binascii

from umqtt.simple import MQTTClient

import wifi
from sensors import temperature
from utils import secrets, utc_time_str
import jwt

broker = "azpi4"
topic = "iaq"

INTERVAL = 60 # seconds


wifi.connect()

def mqtt_connect():
  client = MQTTClient(machine.unique_id().hex(), broker, keepalive=3600)
  client.connect()
  print(f'Connected to {broker} MQTT Broker')
  return client

client = mqtt_connect()

payload = {
  "device": "pico-w",
  "id": machine.unique_id().hex(),
  "value": { "temperature": 0.0 },
  "timestamp": ""
}
secret = binascii.a2b_base64(secrets()["SIGNATURE_SECRET"])

led = machine.Pin("LED", machine.Pin.OUT)


while True:
  led.on()
  payload["value"]["temperature"] = temperature()
  payload["timestamp"] = utc_time_str()
  token = jwt.encode(payload, secret, algorithm='HS256')

  client.publish(topic, token)
  led.off()
  time.sleep(INTERVAL)


