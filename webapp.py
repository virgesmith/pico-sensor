import time
import pico # custom module see https://github.com/virgesmith/pico-c-pymodules
import binascii
import json
from temperature import temperature
import ppwhttp
from ujwt.jwt import Jwt


r = 0
g = 0
b = 0
device_id = binascii.hexlify(pico.id()).decode('utf-8')

with open("secrets.json") as fd:
    creds = json.load(fd)

jwt = Jwt(creds["SIGNATURE_SECRET"])


def timestamp():
    y, mth, d, h, min, s, _x, _y = time.localtime()
    return f"{y:04d}-{mth:02d}-{d:02d}T{h:02d}:{min:02d}:{s:02d}"


@ppwhttp.route("/id", methods=["GET"])
def get_id(method, url):
    return binascii.hexlify(pico.id()).decode('utf-8')


@ppwhttp.route("/temp", methods=["GET"])
def get_id(method, url):
    return jwt.encode({
        "id": device_id,
        "iat": time.time(),
        "temperature": temperature()
    })
    # return f"{temperature():.1f}"


# Edit your routes here
# Nothing fancy is supported, just plain ol' URLs and GET/POST methods
@ppwhttp.route("/", methods=["GET", "POST"])
def get_home(method, url, data=None):
    print(data)
    if method == "POST":
        global r, g, b
        r = int(data.get("r", 0))
        g = int(data.get("g", 0))
        b = int(data.get("b", 0))
        ppwhttp.set_led(r, g, b)
        print(f"Set LED to {r} {g} {b}")

    return f"""<form method="post" action="/">
    <input id="r" name="r" type="number" value="{r}" />
    <input name="g" type="number" value="{g}"  />
    <input name="b" type="number" value="{b}"  />
    <input type="submit" value="Set LED" />
</form>"""


@ppwhttp.route("/test", methods="GET")
def get_test(method, url):
    return "Hello World!"


ppwhttp.start_wifi(creds["WIFI_SSID"], creds["WIFI_PASS"])

server_sock = ppwhttp.start_server()
while True:
    ppwhttp.handle_http_request(server_sock)
    time.sleep(0.01)


# Whoa there! Did you know you could run the server polling loop
# on Pico's *other* core!? Here's how:
#
# import _thread
#
# def server_loop_forever():
#    # Start a server and continuously poll for HTTP requests
#    server_sock = ppwhttp.start_server()
#    while True:
#        ppwhttp.handle_http_request(server_sock)
#        time.sleep(0.01)
#
# Handle the server polling loop on the other core!
# _thread.start_new_thread(server_loop_forever, ())
#
# # Your very own main loop for fun and profit!
# while True:
#     print("Colour: {} {} {}".format(r, g, b))
#     time.sleep(5.0)
