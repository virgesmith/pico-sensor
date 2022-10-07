import time
import machine
import wifi
import jwt
import binascii

from umqtt.simple import MQTTClient

from sensors import temperature
from utils import secrets, utc_time_str

mqtt_broker = "azpi4"
topic = "iaq"
INTERVAL = 300 # seconds


def mqtt_connect():
  print('loading SSL certificate')
  with open("./ca.crt", 'r') as f:
    cert = f.read()
  client = MQTTClient(machine.unique_id().hex(), mqtt_broker, keepalive=3600, ssl=True, ssl_params={"cert": cert})
  client.connect()
  print(f'Connected to {mqtt_broker} MQTT Broker')
  return client


led = machine.Pin("LED", machine.Pin.OUT)
led.on()

creds = secrets()
secret = binascii.a2b_base64(creds["FW_MQTT_SECRET"])
wifi.connect()
client = mqtt_connect()

while True:
  led.on()
  payload = {"device": "pico-w", "id": machine.unique_id().hex(), "value": { "temperature": temperature() }, "timestamp": utc_time_str() }
  token = jwt.encode(payload, secret, algorithm='HS256')
  client.publish(topic, token)
  print(f"published: {payload}")
  led.off()
  time.sleep(INTERVAL)
