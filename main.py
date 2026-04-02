#CANSAT team ProximaAerospace 2026

#import knižníc
from machine import Pin,  SPI ,I2C, UART
from time import sleep, ticks_ms, ticks_diff
from micropyGPS import MicropyGPS
from bmp280 import BMP280I2C, BMP280Configuration
from lora import LoRa
from math import log


#def vstavaná led
led = Pin(25, Pin.OUT)
def blink():
    led.toggle()


#nastavenie BMP280
i2c1_sda = Pin(20)
i2c1_scl = Pin(21)
i2c1 = I2C(0, sda=i2c1_sda, scl=i2c1_scl, freq=400000)
config = BMP280Configuration()
config.pressure_oversampling = BMP280Configuration.PRESSURE_OVERSAMPLING_4X
config.temperature_oversampling = BMP280Configuration.TEMPERATURE_OVERSAMPLING_1X
config.filter_coefficient = BMP280Configuration.FILTER_COEFFICIENT_8
config.power_mode = BMP280Configuration.POWER_MODE_NORMAL
config.standby_time = BMP280Configuration.STANDBY_TIME__5_MS
bmp280_i2c = BMP280I2C(0x76, i2c1) # nechitať!!!nemeniť poradie^

#nastavenie pre GPS
gps = MicropyGPS()
gps_serial = UART(0,baudrate=9600, tx=16, rx= 17)
#v knižnici prepnúť na dd decimálne stupne
            
   #pridať formátovanie
        
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
    frequency=433,
    bandwidth=250000,
    spreading_factor=9,
    coding_rate=5,
)

lora.send('AHOJ krutý svet!test test test test')
 #except:
#   date, gcas, lat, lot, alt, spd, hdop = ("00/00/00",[0, 0, 0.0], 0.0,0.0, 0.0, 0.00, 0.0)
stary_cas = 0.0


def main():
    global stary_cas
    
    while True:
        while gps_serial.any():
            #b=ticks_ms()c
            data = gps_serial.readline()
            #print(data)
            for byte in data:
                stat = gps.update(chr(byte))
                if stat is not None:
                    cas = gps.timestamp[2]
                    if stary_cas  != cas:
                        blink()
                        date, gcas, lat, lot, alt, spd, hdop = gps.date_string('short'), gps.timestamp, gps.latitude[0], gps.longitude[0], gps.altitude, '{:02.2f}'.format(gps.speed[2]), gps.hdop
                        stary_cas = cas
                        
                        #debug
#                         print(date, gcas)
#                         print('lat:',lat)
#                         print('lot:',lot)
#                         print('alt',alt)
#                         print('spd',spd)
#                         print('hdop',hdop)
#                         print()
                        readout = bmp280_i2c.measurements
                        t, p = readout['t'], readout['p'] # vypočítať nadmorskú výšku
                        a=ticks_ms()
                        #lat = str(lat)
                        lora.send(bytearray(str(t).encode(),',',str(t).encode(p)))
                        print(ticks_diff(ticks_ms(),a))
#                         print(t ,p )
#                         print(f"Temperature: {readout['t']} °C, pressure: {readout['p']} hPa",'\n')
                        
                        #print(machine.freq())
                                                             
main()