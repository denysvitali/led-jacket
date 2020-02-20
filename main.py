import time
import utime
import math
import network
import machine
import picoweb
import uasyncio as asyncio
import machine, neopixel
from machine import ADC, Pin


def wheel(pos):
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return 255 - pos * 3, pos * 3, 0
    if pos < 170:
        pos -= 85
        return 0, 255 - pos * 3, pos * 3
    pos -= 170
    return pos * 3, 0, 255 - pos * 3


def brightness(brightness, arr):
    return [math.ceil(x * brightness) for x in arr]


app = picoweb.WebApp(__name__)

# Setup Wi-Fi

ap = network.WLAN(network.AP_IF)  # create access-point interface
ap.config(essid='LED Jacket by @denvit', authmode=3, password='led-or-not')  # set the ESSID of the access point
ap.config(max_clients=10)  # set how many clients can connect to the network
ap.active(True)  # activate the interface

mic_gain = Pin(32, mode=Pin.OUT, value=False)


@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Hello world from picoweb running on the ESP32")


@app.route("/sensitivity/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Hello world from picoweb running on the ESP32")


@asyncio.coroutine
def server_loop():
    print("Server started!")
    app.run(debug=False, host="0.0.0.0", port=80)


@asyncio.coroutine
def ledLoop():
    print("Led Loop")
    yield
    np_len = 200
    np = neopixel.NeoPixel(machine.Pin(0), np_len)

    for i in range(np_len):
        np[i] = (0, 0, 0)

    np.write()

    adc = ADC(Pin(33))

    rst_pin = Pin(13, mode=Pin.OUT, value=False)
    strobe_pin = Pin(12, mode=Pin.OUT, value=False)

    # Init sequence
    rst_pin.on()
    utime.sleep_us(5)  # 100ns Minimum
    rst_pin.off()

    octave = [0] * 7
    lower_bound = 20

    # We'll use only:
    # - octave[0] = 63 Hz     Low
    # - octave[3] = 1000 Hz   Mid
    # - octave[5] = 6250 Hz   Treble

    bands_array = [0, 3, 5]

    while True:
        yield
        for i in range(7):
            strobe_pin.off()
            utime.sleep_us(36)  # minimum pulse width = 18us
            octave[i] = adc.read_u16()
            strobe_pin.on()
            utime.sleep_us(100)  # Strobe to strobe

        # Save Octave result to LED
        # 7 bands, np_led LEDs

        bands = len(bands_array)
        led_per_band = math.floor(np_len / bands)

        average_octave = octave

        offset = 0
        for b in range(bands):
            # Each octave
            i = bands_array[b]

            if octave[i] != 0:
                threshold = math.floor(led_per_band * (average_octave[i] - lower_bound) / (65535 - lower_bound))
            else:
                threshold = led_per_band
                octave[i] = 65536

            if threshold < 0:
                threshold = 0

            for j in range(led_per_band):
                if j <= threshold:
                    rc_index = (offset * 256 // np_len) + j
                    np[offset + j] = brightness(0.2, wheel(rc_index & 255))
                else:
                    np[offset + j] = (0, 0, 0)
            offset = offset + led_per_band
        # print(octave)
        np.write()
        utime.sleep_us(10)

    # demo(np, np_len)


loop = asyncio.get_event_loop()
loop.create_task(ledLoop())
loop.create_task(server_loop())
loop.run_forever()
