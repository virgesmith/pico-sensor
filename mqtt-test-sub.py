import base64
import paho.mqtt.client as mqtt

import jwt

from utils import secrets

key = base64.b64decode(secrets()["SIGNATURE_SECRET"])

def on_connect(client, userdata, message, return_code):
    """
    Called when the broker responds to our connection request.

    @param client:
        the client instance for this callback
    @param userdata:
        the private user data as set in Client() or userdata_set()
    @param message:
        response message sent by the broker
    @param return_code:
        the connection result
    """

    # This will be called once the client connects
    print(f"Connected with result code {return_code}")
    # Subscribe
    for topic in userdata["topics"]:
        print(f"subscribing to: {topic}")
        client.subscribe(topic)

def on_message(client, userdata, message):
    """
    Called when a message has been received on a topic that the client subscribes to.
    This callback will be called for every message received.

    @param client:
        the client instance for this callback
    @param userdata:
        the private user data as set in Client() or userdata_set()
    @param message:
        an instance of MQTTMessage.
        This is a class with members topic, payload, qos, retain.
    """
    print(f"Message received [{message.topic}]:")
    try:
        data = jwt.decode(message.payload, key, algorithms=['HS256'])
    except jwt.PyJWTError as e:
        print(e)
    else:
        print(data)


mqtt_broker ="azpi4"

client = mqtt.Client("mqtt-test-subscriber", userdata={"topics": ["iaq"]})
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker)
client.loop_forever()  # Start networking daemon

