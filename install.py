import network
import ujson
import upip
import rp2

with open("secrets.json","r") as fh:
  creds = ujson.load(fh)

rp2.country("GB")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(creds["WIFI_SSID"], creds["WIFI_PASS"])


# upip.install(‘ujwt’)
upip.install(‘umqtt.simple’)