#CANSAT team ProximaAerospace 2026
#ground station
#import knižníc

from machine import Pin,  SPI 
from time import sleep, ticks_ms, ticks_diff
from lora import LoRa



#def vstavaná led
led = Pin(25, Pin.OUT)
led_vonku = Pin(21, Pin.OUT)
def blink():
    led.toggle()
    led_vonku.toggle()
      
#nastavenie pre lora
      
SCK = 2
MOSI = 3
MISO = 4
CS = 5 # NSS
RX = 6
spi = SPI(
    0, baudrate=10000000,
    sck=Pin(SCK, Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(MOSI, Pin.OUT, Pin.PULL_UP),
    miso=Pin(MISO, Pin.IN, Pin.PULL_UP),
)
spi.init()

lora = LoRa(
    spi,
    cs=Pin(CS, Pin.OUT),
    rx=Pin(RX, Pin.IN),
    frequency=433.4,
    bandwidth=250000,
    spreading_factor=9,
    coding_rate=5,
    preamble_length=8,
    crc = True, 
    #nastavenia musia byť identické na oby dvoch
    
)

lora.recv()




led.on()
led_vonku.on()
print('príjem')
def main(frame):
    blink()
    try:
        print(frame.decode("utf-8")+',',lora.get_rssi())
        
    except:
        pass
    
                                                      
lora.on_recv(main)

