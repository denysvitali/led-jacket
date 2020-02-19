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

np_len = 50
np = neopixel.NeoPixel(machine.Pin(0), np_len)

for i in range(np_len):
  np[i] = (0, 0, 0)

np.write()

adc = ADC(Pin(33))

rst_pin = Pin(13, mode=Pin.OUT, value=False)
strobe_pin = Pin(12, mode=Pin.OUT, value=False)

# Init sequence
rst_pin.value(True)
time.sleep_us(5) # 100ns Minimum
rst_pin.value(False)

octave = [0] * 7

animation_duration = 5
lastPeak = [animation_duration] * 7

lowBound = 500

while True:
  for i in range(7):
    strobe_pin.value(False)
    utime.sleep_us(35) # minimum pulse width = 18us
    octave[i] = adc.read_u16()
    strobe_pin.value(True)
    utime.sleep_us(100) # Strobe to strobe
  

  # Save Octave result to LED
  # 7 bands, np_led leds

  bands = 7

  led_per_band = math.floor(np_len / bands)

  offset = 0
  for i in range(bands):
    # Each octave

    rc_index = i * 256 // bands
    threshold = math.floor(led_per_band * (octave[i]-lowBound)/(65535-lowBound))
    
    if threshold < 0:
      threshold = 0
    
    for j in range(led_per_band):
      if(j+1 <= threshold):
        #rc_index = (offset * 256 // np_len) + j
        #np[offset + j] = wheel(rc_index & 255)

        np[offset + j] = wheel(rc_index & 255)
      else:
        np[offset + j] = (0, 0, 0)
    offset = offset + led_per_band
  #print(octave)
  np.write()
  time.sleep_us(40)

#demo(np, np_len)