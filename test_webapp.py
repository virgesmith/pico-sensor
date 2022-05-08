
import jwt
import json
import requests
from datetime import datetime
from time import sleep

with open("secrets.json") as fd:
  secret = json.load(fd)["SIGNATURE_SECRET"]

DEVICE_URL="http://azpico"

resp = requests.get(f"{DEVICE_URL}/temp")

resp.raise_for_status()

print(resp.text)

result = jwt.decode(resp.text, key=secret, algorithms="HS256")

# NB pico is not TZ aware/timestamp is incorrect
print(f'{result["temperature"]:.1f}C @ {datetime.fromtimestamp(result["iat"]).isoformat()}')

requests.post(f"{DEVICE_URL}/", data={"r": 255, "g": 0, "b": 0})
sleep(1)

requests.post(f"{DEVICE_URL}/", data={"r": 0, "g": 255, "b": 0})
sleep(1)

requests.post(f"{DEVICE_URL}/", data={"r": 0, "g": 0, "b": 255})
sleep(1)