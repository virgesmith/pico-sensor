# pico-sensor

Playing with a raspberry pi [pico](https://www.raspberrypi.com/products/raspberry-pi-pico/) with the [pico-wireles](https://shop.pimoroni.com/products/pico-wireless-pack?variant=32369508581459) board... serving wildly inaccurate temperature readings using micropython

JWT implementation from https://github.com/s-binetruy/micropython-jwt

Secret was generated using

```sh
openssl rand -base64 16
# or alternatively cat /dev/urandom|head -c 16|base64
```

## webapp

`/temp` endpoint Returns a JWT-encoded temperature reading. Use test_webapp to decode and verify it.


