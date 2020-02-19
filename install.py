import network
 
def connect():
  ssid = "denvit"
  password =  "espressif"
 
  station = network.WLAN(network.STA_IF)
 
  if station.isconnected() == True:
      print("Already connected")
      return
 
  station.active(True)
  station.connect(ssid, password)
 
  while station.isconnected() == False:
      pass
 
  print("Connection successful")
  print(station.ifconfig())

connect()

import upip
upip.install('micropython-uasyncio')
upip.install('micropython-pkg_resources')