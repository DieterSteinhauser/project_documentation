# -----------------------------------------
#                 NOTES 
# -----------------------------------------
"""
Dieter Steinhauser
11/2022
Design 1
Ultrasonic Theremin

This program employs talks to various peripherals to create a theremin music device.

The Major components include:
Transfers of SPI data to DAC
LCD status
ADC conversions
Switch inputs
button inputs
Overclocking

Potentially:
multithreading
DMA

"""

# -----------------------------------------
#               IMPORTS
# -----------------------------------------

from LCD import *
from LUT import *
from spi_config import *
import _thread
from utime import sleep, sleep_ms, sleep_us, ticks_ms
from machine import Pin, Timer, ADC, freq

# -----------------------------------------
#         CONSTANTS/VARIABLES
# -----------------------------------------   

# ------------------
REFRESH_RATE = 60 # Frequency in Hz
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
FREQ_MAX = 100
FREQ_MIN = 10
AMP_MAX = DAC_REF
AMP_MIN = 0

MAX_DIST_US0 = 50
MAX_DIST_US1 = 20

# -----------------------------------------
#           METHODS
# -----------------------------------------

def append_space(string, length):
    while (len(string) < length):
        string = ' ' + string
    return string

# -------------------------------------------------------------
#           INITIALIZATION
# -------------------------------------------------------------

# -----------------------------------------
#           SYSTEM CLOCK
# -----------------------------------------

DEFAULT_SYS_CLK = 125_000_000
STABLE_OVERCLOCK = 270_000_000

# Pico can go up to 270MHz before needing to flash to the eeprom directly.
system_clock = STABLE_OVERCLOCK

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
sw0 = Pin(10, Pin.IN, Pin.PULL_DOWN)
sw1 = Pin(11, Pin.IN, Pin.PULL_DOWN)
sw2 = Pin(12, Pin.IN, Pin.PULL_DOWN)
sw3 = Pin(13, Pin.IN, Pin.PULL_DOWN)
switch_pins = [sw0, sw1, sw2, sw3]

# LEDs
# ----------------------------
led0 = Pin(14, Pin.OUT)
led1 = Pin(15, Pin.OUT)
led_onboard = Pin(25, Pin.OUT)
led_pins = [led0, led1, led_onboard]

# SPI handled by the Hardware in spi_config.py
# ----------------------------
# miso = Pin(16, Pin.IN)
# cs = Pin(17, Pin.OUT, value=1)
# mosi = Pin(18, Pin.OUT)
# sck = Pin(19, Pin.OUT)

# Buttons
# ----------------------------
button0 = Pin(20, Pin.IN)
button1 = Pin(21, Pin.IN)
button2 = Pin(22, Pin.IN)
button3 = Pin(28, Pin.IN)
button_pins = [button0, button1, button2, button3]

# ADC
# ----------------------------
# adc0 = ADC(26) # Connect to GP26, which is channel 0
# adc1 = ADC(27) # Connect to GP27, which is channel 1


# -----------------------------------------
#           GENERAL I/O 
# -----------------------------------------
last_time = 0
def debounce():
    global last_time
    new_time = ticks_ms()
    # if it has been more that 1/10 of a second since the last event, we have a new event
    if (new_time - last_time) > 100: 
        last_time = new_time
        return True
    else:
        return False

def button0_irq_handler(pin):
    global reset
    if (debounce()):
        reset = True

def button1_irq_handler(pin):
    global menu_select
    if (debounce()):
        menu_select = 0

def button2_irq_handler(pin):
    global menu_select
    if (debounce()):
        menu_select = 1

def button3_irq_handler(pin):
    global menu_select
    if (debounce()):
        menu_select = 2

# now we register the handler function when the button is pressed
button0.irq(trigger=Pin.IRQ_RISING, handler = button0_irq_handler)
button1.irq(trigger=Pin.IRQ_RISING, handler = button1_irq_handler)
button2.irq(trigger=Pin.IRQ_RISING, handler = button2_irq_handler)
button3.irq(trigger=Pin.IRQ_RISING, handler = button3_irq_handler)


# -----------------------------------------
#           ULTRASONIC SENSORS
# -----------------------------------------


from machine import Pin
from utime import ticks_us, sleep_us

# Ultrasonic sensor pins
# ----------------------------
us0_trig = Pin(6, Pin.OUT)
us0_echo = Pin(7, Pin.IN)
us1_trig = Pin(8, Pin.OUT)
us1_echo = Pin(9, Pin.IN)

def get_distance_u0():

    # send the trigger wave
    us0_trig(1)
    sleep_us(1)
    us0_trig(0)
    
    # listen for the return echo
    while us0_echo.value() == 0:
        start = ticks_us()
    while us0_echo.value() == 1:
        stop = ticks_us()

    return ((stop - start) * 0.0343) / 2

def get_distance_u1():
    global us1_distance

    # send the trigger wave
    us1_trig(1)
    sleep_us(1)
    us1_trig(0)
    
    # listen for the return echo
    while us1_echo.value() == 0:
        start = ticks_us()
    while us1_echo.value() == 1:
        stop = ticks_us()

    return ((stop - start) * 0.0343) / 2


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
#           DAC
# -----------------------------------------
index = 0
selected_wave = None


# -----------------------------------------
#           TIMERS
# -----------------------------------------
spi_timer = Timer()

def spi_timer_tick(timer):
    """Process that sends waveform data to the DAC via SPI"""
#     spi_timer.init(freq=frequency*selected_wave.size, mode=Timer.PERIODIC, callback=spi_timer_tick)

    global frequency
    global amplitude
    global selected_wave
    global index
    global cs

    if selected_wave is not None:
    
        # output the waveform to DAC via SPI  
                
        # complete math for the value that we send to the DAC
        dac_output = int((selected_wave.lut[index] * (amplitude / AMP_MAX)) + DC_OFFSET_RES)
        
        # bit shift so the value is acceptable by the 10 bit DAC
        
        # A3 A2 A1 A0 D10 D9 D8 D7 D6 D5 D4 D3 D2 D1 D0 X1 X0
        word = (0x9 << 12) + (dac_output << 2)
        format_array = [((word & 0xFF00) >> 8 ), (word & 0x00FF)]
        write_array = bytearray(format_array)

        # write to the device
        cs(0)
        spi.write(write_array)
        cs(1)
                
        # iterate through the waveform tables.
        index += 1
        index &= selected_wave.last_index


# -----------------------------------------
#           PROCESS 1: IO
# -----------------------------------------


while True:

    splash = True
    # Display the splash screen on startup.
    if splash is True:
        led0(1)
        led1(1)
        led_onboard(1)
        lcd_puts(f'USonic Theremin  ')
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
        led0.toggle()
        led1.toggle()
        led_onboard.toggle()

    # Start timers and threads 
    reset = False
    menu_select = 0
    saved_frequency = 0
    frequency = 0
    amplitude = 0
    freq_min = FREQ_MIN
    freq_max = FREQ_MAX
    amp_max = AMP_MAX
    amp_min = AMP_MIN

    # -----------------------------------------
    #           Core Loop with reset
    # -----------------------------------------
    while reset is False:
    

        # read ADC rotary controls
        # -----------------------------------------
        adc0_reading = 3.3 - (adc0.read_u16() * VOLT_PER_BIT)
        adc1_reading = 3.3 - (adc1.read_u16() * VOLT_PER_BIT)
        # print(f'ADC0: {adc0_reading}')
        # print(f'ADC1: {adc1_reading}')
        
        # Read Ultrasonic Sensors
        # -----------------------------------------
        us0_distance = get_distance_u0()
        us1_distance = get_distance_u1()
        # print(f'US0: {us0_distance}')
        # print(f'US1: {us1_distance}')
        
        # read switch controls and get selected wave
        # -----------------------------------------
        switch_list = []
        for switch in switch_pins:
            switch_list.append(switch()) # read switch and put val in list
        
        if switch_list.count(1) != 1: # if none of the switches are high.
            selected_wave = None
            
        else:
            switch_key = "SW" + str(switch_list.index(1))
            selected_wave = waveforms.get(switch_key)
        
        # MENU LOGIC
        # -----------------------------------------
        
        if menu_select == 0: # Default Menu, Show wave and frequency
            
            wave_str = f'Wave: None      ' if selected_wave is None else f'Wave: {selected_wave.name}'
            
            # display the current waveform and frequency
            # -----------------------------------------
            lcd_puts(wave_str)
            lcd_goto(0,1)
            lcd_puts(f'F: {frequency}Hz A: {amplitude}V      ')
            lcd_home()
            
        elif menu_select == 1: # Change range of waveform frequency
            
            freq_min = round((FREQ_MAX) * (adc0_reading / ADC_REF), 1)
            freq_max = round((FREQ_MAX) * (adc1_reading / ADC_REF), 1)
            
            # display the upper bound and lower bound
            # -----------------------------------------
            lcd_puts(f'Upper: {freq_max}Hz     ')
            lcd_goto(0,1)
            lcd_puts(f'Lower: {freq_min}Hz     ')
            lcd_home()
            
        elif menu_select == 2:
            
            amp_min = round(AMP_MAX * (adc0_reading / ADC_REF), 1)
            amp_max = round((AMP_MAX) * (adc1_reading / ADC_REF), 1)
            
            # display the upper bound and lower bound
            # -----------------------------------------
            lcd_puts(f'Upper: {amp_max}V     ')
            lcd_goto(0,1)
            lcd_puts(f'Lower: {amp_min}V     ')
            lcd_home()                
            
            
        # Dual Core Interaction
        # -----------------------------------------
        
        #  out of range, stop the waveform process.
        if us1_distance > MAX_DIST_US1 or us0_distance > MAX_DIST_US0:
            # spi_timer.deinit()
            frequency = 0
            amplitude = 0
            
        else:
            frequency = round(((freq_max - freq_min) * ((MAX_DIST_US0 - us0_distance) / MAX_DIST_US0)) + freq_min)
            amplitude = round(((amp_max - amp_min) * ((MAX_DIST_US1 - us1_distance) / MAX_DIST_US1)) + amp_min, 1)
        
            if selected_wave != None:
                spi_timer.init(freq=frequency*selected_wave.size, mode=Timer.PERIODIC, callback=spi_timer_tick)
            else:
                spi_timer.deinit()
        
        # toggle onboard LED for System speed status and refresh delay
        # -----------------------------------------
        led_onboard.toggle()
        utime.sleep_ms(REFRESH_PERIOD)
        
    spi_timer.deinit()
  
# -----------------------------------------
#     PROCESS 2: Waveform Generation
# -----------------------------------------

# while True:
#     if frequency != 0:
#         
#         if frequency != saved_frequency and selected_wave is not None:  
#          spi_timer.init(freq=frequency*selected_wave.size, mode=Timer.PERIODIC, callback=spi_timer_tick)
#          saved_frequency = frequency
#          
#     else:
#         spi_timer.deinit()
# 
#     
    
    
# -----------------------------------------
#           END OF FILE
# -----------------------------------------


