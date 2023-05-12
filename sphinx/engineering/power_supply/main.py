# -----------------------------------------
#                 NOTES 
# -----------------------------------------
"""
Dieter Steinhauser
12/2022
PicoPAD Test Script

"""

# -----------------------------------------
#               IMPORTS
# -----------------------------------------

from LCD import *
# import _thread
from utime import sleep, sleep_ms, sleep_us, ticks_ms
from machine import Pin, Timer, ADC, freq
# import gc

# -----------------------------------------
#         CONSTANTS/VARIABLES
# -----------------------------------------   

# ------------------
REFRESH_RATE = 360 # Frequency in Hz
REFRESH_PERIOD = int((1 / REFRESH_RATE) * 1000) # delay in milliseconds

# ------------------
UPY_BIT_RES = 16
ADC_REF = 3.3
VOLT_PER_BIT = ADC_REF / (2**UPY_BIT_RES) # ADC recieves in 2 byte packets and micropython automagically fixes it.

# ------------------
DAC_REF = 5.0
DC_OFFSET = 0
DC_OFFSET_RES = int((DC_OFFSET / DAC_REF) * (2**UPY_BIT_RES))

# ------------------
FREQ_MAX = 160
FREQ_MIN = 10
AMP_MAX = DAC_REF
AMP_MIN = 0

MAX_DIST_US0 = 50
MAX_DIST_US1 = 20


# -------------------------------------------------------------
#           INITIALIZATION
# -------------------------------------------------------------

# -----------------------------------------
#           SYSTEM CLOCK
# -----------------------------------------

UNDERCLOCK = 30_000_000
DEFAULT_SYS_CLK = 125_000_000
STABLE_OVERCLOCK = 270_000_000

# Pico can go up to 270MHz before needing to flash to the eeprom directly.
system_clock = DEFAULT_SYS_CLK

# if the system clock is not the default, apply the clock speed.
if system_clock !=  DEFAULT_SYS_CLK:
    freq(system_clock)

# print(f'Clock: {freq()/1e6}MHz')

# -----------------------------------------
#               PINOUT
# -----------------------------------------

# LCD Pins handled in LCD.py
# ----------------------------
# EN = Pin(0, Pin.OUT)
# RS = Pin(1, Pin.OUT)
# D7 = Pin(2, Pin.OUT)
# D6 = Pin(3, Pin.OUT)
# D5 = Pin(4, Pin.OUT)
# D4 = Pin(5, Pin.OUT)

# Ultrasonic sensor pins handled in sensors.py
# ----------------------------
# us0_trig = Pin(6, Pin.OUT)
# us0_echo = Pin(7, Pin.IN)
# us1_trig = Pin(8, Pin.OUT)
# us1_echo = Pin(9, Pin.IN)

# Switches
# ----------------------------
# sw0 = Pin(10, Pin.IN, Pin.PULL_DOWN)
# sw1 = Pin(11, Pin.IN, Pin.PULL_DOWN)
# sw2 = Pin(12, Pin.IN, Pin.PULL_DOWN)
# sw3 = Pin(13, Pin.IN, Pin.PULL_DOWN)
# switch_pins = [sw0, sw1, sw2, sw3]

# LEDs
# ----------------------------
# led0 = Pin(14, Pin.OUT)
# led1 = Pin(15, Pin.OUT)
led_onboard = Pin(25, Pin.OUT)
output_en = Pin(16, Pin.OUT)
# led_pins = [led0, led1, led_onboard]

# SPI handled by the Hardware in spi_config.py
# ----------------------------
# miso = Pin(16, Pin.IN)
# cs = Pin(17, Pin.OUT, value=1)
# mosi = Pin(18, Pin.OUT)
# sck = Pin(19, Pin.OUT)

# Buttons
# ----------------------------
# button0 = Pin(20, Pin.IN)
# button1 = Pin(21, Pin.IN)
# button2 = Pin(22, Pin.IN)
# button3 = Pin(28, Pin.IN)
# button_pins = [button0, button1, button2, button3]

# ADC
# ----------------------------
# adc0 = ADC(26) # Connect to GP26, which is channel 0
# adc1 = ADC(27) # Connect to GP27, which is channel 1

# -----------------------------------------
#           LCD
# -----------------------------------------
lcd_init()
lcd_clear()
# lcd_cursor_on()
# lcd_cursor_blink()
# -----------------------------------------
#           ADC
# -----------------------------------------
adc1 = ADC(26) # Connect to GP26, which is channel 0
adc0 = ADC(27) # Connect to GP27, which is channel 1
# adc2 = machine.ADC(28) # Connect to GP28, which is channel 2
# adc_reading = adc0.read_u16() * VOLT_PER_BIT # read and report the ADC reading

# -----------------------------------------
#           SD CARD VIA SPI
# -----------------------------------------
# 
# import sdcard
# import os
# import uos
# 
# # Assign chip select (CS) pin (and start it high)
# cs = Pin(20, machine.Pin.OUT)
# 
# # Intialize SPI peripheral (start with 1 MHz)
# spi = machine.SPI(0,
#                   baudrate=1000000,
#                   polarity=0,
#                   phase=0,
#                   bits=8,
#                   firstbit=machine.SPI.MSB,
#                   sck=Pin(18),
#                   mosi=Pin(19),
#                   miso=Pin(16))
# 
# # Initialize SD card
# sd = sdcard.SDCard(spi, cs)
# 
# vfs = uos.VfsFat(sd)
# uos.mount(vfs, "/sd")
# 
# # Create a file and write something to it
# file = open("/sd/test01.txt", "w")
# 
# with open("/sd/test01.txt", "w") as file:
#     file.write("Hello, SD World!\r\n")
#     file.write("This is a test\r\n")
# 
# # Open the file we just created and read from it
# with open("/sd/test01.txt", "r") as file:
#     data = file.read()
#     print(data)

# -----------------------------------------
#           PROCESS 1: IO
# -----------------------------------------

while True:

    splash = True
    # Display the splash screen on startup.
    if splash is True:
        led_onboard(1)
        lcd_puts(f'Linear Supply   ')
        lcd_goto(0,1)
        lcd_puts(f'20V/3A Dieter S.')
        sleep(2)
        lcd_home()
        lcd_clear()
        led_onboard.toggle()
        
    list_length = 100
    counter = 0
    current_list = []
    voltage_list = []
    while True:

        # read ADC
        # -----------------------------------------
        
        adc0_reading = (adc0.read_u16() * VOLT_PER_BIT)
        adc1_reading = (adc1.read_u16() * VOLT_PER_BIT)
        
        voltage = (adc1_reading - 0.010) * 7.2962
        current = (adc0_reading - 0.010)

        current_list.append(current)
        voltage_list.append(voltage)
        counter += 1
        
        if counter == list_length:
            
 
            current = sum(current_list)/ len(current_list)
            voltage = sum(voltage_list)/ len(voltage_list)
            
            current = round(current, 3)
            voltage = round(voltage, 3)

            if current <= 0:
                current = 0

            if voltage < 0.9:
                voltage = 0
                current = 0
                output_en(0)
            else:
                output_en(1)
                
            counter = 0
            current_list = []
            voltage_list = []
            
            lcd_home()
            lcd_puts(f'A: {current}A       ')
            lcd_goto(0,1)
            lcd_puts(f'V: {voltage}V       ')
            
        # toggle onboard LED for System speed status and refresh delay
        # -----------------------------------------
        led_onboard.toggle()
        utime.sleep_ms(REFRESH_PERIOD)
        # gc.collect()




