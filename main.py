import time
import utime
import math

def wheel(pos):
  if pos < 0 or pos > 255:
    return (0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait, np_len):
  for j in range(255):
    for i in range(np_len):
      rc_index = (i * 256 // np_len) + j
      np[i] = wheel(rc_index & 255)
    np.write()
    time.sleep_ms(wait)

def demo(np, np_len):
    rainbow_cycle(1, np_len)

import machine, neopixel
from machine import ADC, Pin

np_len = 30
np = neopixel.NeoPixel(machine.Pin(0), np_len)

for i in range(np_len):
  np[i] = (255, 0, 255)

np.write()

adc = ADC(Pin(33))

rst_pin = Pin(13, mode=Pin.OUT, value=False)
strobe_pin = Pin(12, mode=Pin.OUT, value=False)

# Init sequence
rst_pin.value(True)
strobe_pin.value(True)

utime.sleep_us(20) # 18us Minimum
strobe_pin.value(False)
time.sleep_us(5) # 100ns Minimum

rst_pin.value(False)
utime.sleep_us(80) # reset to strobe, minimum 72us
# trs
strobe_pin.value(True)
utime.sleep_us(80) # 72us Minimum, 18us per strobe pulse width
strobe_pin.value(False)

utime.sleep_us(80) # Strobe to strobe

prevOctave = [0] * 7
octave = [0] * 7

animation_duration = 5
lastPeak = [animation_duration] * 7

while True:
  prevOctave = octave
  for i in range(7):
    strobe_pin.value(True)
    utime.sleep_us(20) # minimum pulse width = 18us
    octave[i] = adc.read_u16()
    strobe_pin.value(False)
    utime.sleep_us(80) # Strobe to strobe
  

  # Save Octave result to LED
  # 7 bands, np_led leds

  led_per_band = math.floor(np_len / 7)

  offset = 0
  for i in range(7):
    # Each octave

    if octave[i] == 0:
      # PEAK!
      lastPeak[i] = 0
      print("octave " + str(i) + ": PEAK!")
    else:
      lastPeak[i]+= 1
      if lastPeak[i] > animation_duration:
        lastPeak[i] = animation_duration

    threshold = (1 - lastPeak[i] / animation_duration) * led_per_band

    for j in range(led_per_band):
      if(j+1 <= threshold):
        rc_index = (offset * 256 // np_len) + j
        np[offset + j] = wheel(rc_index & 255)
      else:
        np[offset + j] = (0, 0, 0)
    offset = offset + led_per_band

  np.write()
  time.sleep_ms(20)

#demo(np, np_len)