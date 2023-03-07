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
import gc
from machine import RTC



# -----------------------------------------
#         CONSTANTS/VARIABLES
# -----------------------------------------   

# ------------------
REFRESH_RATE = 10 # Frequency in Hz
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
#           REAL TIME CLOCK
# -----------------------------------------
# from machine import RTC

rtc = RTC()
rtc.datetime((2022, 12, 22, 0, 12, 52, 0, 0)) # set a specific date and
                                             # time, eg. 2017/8/23 1:12:48
rtc.datetime() # get date and time

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
adc0 = ADC(26) # Connect to GP26, which is channel 0
adc1 = ADC(27) # Connect to GP27, which is channel 1
# adc2 = machine.ADC(28) # Connect to GP28, which is channel 2
# adc_reading = adc0.read_u16() * VOLT_PER_BIT # read and report the ADC reading


# -----------------------------------------
#           PROCESS 1: IO
# -----------------------------------------

while True:

    splash = True
    # Display the splash screen on startup.
    if splash is True:
        led_onboard(1)
        lcd_puts(f'PicoPAD Test  ')
        lcd_goto(0,1)
        lcd_puts(f'Dieter S.        ')
        sleep(2)
        lcd_home()
        lcd_clear()
        lcd_puts(f'System Clock')
        lcd_goto(0,1)
        lcd_puts(f'{freq()/1e6}MHz')
        sleep(2)
        lcd_home()
        lcd_clear()
        led_onboard.toggle()

    while True:

        # read ADC
        # -----------------------------------------
#         adc0_reading = (adc0.read_u16() * VOLT_PER_BIT) - 0.100
#         adc1_reading = (adc1.read_u16() * VOLT_PER_BIT) - 0.100

        year, month, day, weekday, hour, minute, second, microsecond = rtc.datetime() # get date and time
        hour = f'0{hour}' if hour < 10 else hour
        minute = f'0{minute}' if minute < 10 else minute
        second = f'0{second}' if second < 10 else second
        microsecond = f'0{microsecond}' if microsecond < 10 else microsecond
        
        lcd_home()
        lcd_puts(f'{month}/{day}/{year}   ')
        lcd_goto(0,1)
        lcd_puts(f'{hour}:{minute}:{second}   ')
        
        # toggle onboard LED for System speed status and refresh delay
        # -----------------------------------------
        led_onboard.toggle()
        utime.sleep_ms(REFRESH_PERIOD)
        gc.collect()




