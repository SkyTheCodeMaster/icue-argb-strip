from __future__ import annotations

import time

import serial # type: ignore
from cuesdk import * # type: ignore

sdk = CueSdk()

sdk.connect(lambda evt: print(evt.state))

time.sleep(0.1)

devices,err = sdk.get_devices(
  CorsairDeviceFilter(
    device_type_mask=CorsairDeviceType.CDT_FanLedController
  ) 
) # type: ignore
print(err)
device = devices[0]
device_id: str = device.device_id # type: ignore
positions: list[CorsairLedPosition] = sdk.get_led_positions(device_id)[0]

last_packet = bytes()

ser = serial.Serial("COM3",2000000,timeout=1)

def get_leds() -> list[CorsairLedColor]:
  leds = sdk.get_led_colors(device_id, positions)[0]
  return leds[-50:]

def byte(x: int) -> bytes:
  return x.to_bytes(1,"big")

def send_leds() -> None:
  global last_packet
  leds: list[CorsairLedColor] = get_leds()
  packet = bytes()
  for led in leds:
    packet += byte(led.r)
    packet += byte(led.g)
    packet += byte(led.b)
  # check if it's the same packet to save bandwidth
  if packet == last_packet:
    return
  else:
    last_packet = packet
    ser.write(packet)
  # now wait for arduino to say ok
  ok = False
  while not ok:
    data = ser.read(2).decode()
    print("got ok, sending more data")
    ok = data == "ok"

def main() -> None:
  while True:
    send_leds() # this sends 200 bytes / 1600 bits of data down serial.
    # this is a total of 192000 baud at 120fps, which is fine for the serial bus of 230400 baud.
main()