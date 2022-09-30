import machine
import time
import ujson

from umqtt.simple import MQTTClient

import wifi
from sensors import temperature
from utils import secrets, utc_time_str

broker = "azpi4"
topic = "test"

INTERVAL = 3 # seconds


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

led = machine.Pin("LED", machine.Pin.OUT)

while True:
  led.on()
  payload["value"]["temperature"] = temperature()
  payload["timestamp"] = utc_time_str()
  client.publish(topic, ujson.dumps(payload))
  led.off()
  time.sleep(INTERVAL)


