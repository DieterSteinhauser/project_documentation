#--------------------------------------------------
#       PARALLEL LCD FUNCTIONS
#       ======================
#
# These functions initialize and control the LCD
#
# Author: Dogan Ibrahim
# File  : LCD
# Date  : August, 2021
#--------------------------------------------------
# Modified by Dieter Steinhauser
#--------------------------------------------------
from machine import Pin
import utime

# ----------------------
LCD_CMD = 0
LCD_DATA = 1
# ----------------------

# GPIO Wiring
# ----------------------

#! Wiring here is backwards because of issues in layout.
EN = Pin(0, Pin.OUT)
RS = Pin(1, Pin.OUT)
D4 = Pin(5, Pin.OUT)
D5 = Pin(4, Pin.OUT)
D6 = Pin(3, Pin.OUT)
D7 = Pin(2, Pin.OUT)
PORT = [5, 4, 3, 2]
L = [0,0,0,0]


# Methods
# ----------------------

def Configure():

    for i in range(4):
       L[i] = Pin(PORT[i], Pin.OUT)
    
def lcd_strobe():

    EN.value(1)
    utime.sleep_ms(1)
    EN.value(0)
    utime.sleep_ms(1)
    
def lcd_write(c, mode):

    if mode == 0:
       d = c
    else:
       d = ord(c)
    d = d >> 4
    for i in range(4):
        b = d & 1
        L[i].value(b)
        d = d >> 1
    RS.value(mode)
    lcd_strobe()
    
    if mode == 0:
       d = c
    else:
       d = ord(c)
    for i in range(4):
        b = d & 1
        L[i].value(b)
        d = d >> 1
    RS.value(mode)
    lcd_strobe()
    utime.sleep_ms(1)
    RS.value(1)

def lcd_clear():

    lcd_write(0x01, 0)
    utime.sleep_ms(5)

def lcd_home():

    lcd_write(0x02, 0)
    utime.sleep_ms(5)

def lcd_cursor_blink():

    lcd_write(0x0D, 0)
    utime.sleep_ms(1)

def lcd_cursor_on():

    lcd_write(0x0E, 0)
    utime.sleep_ms(1)

def lcd_cursor_off():

    lcd_write(0x0C, 0)
    utime.sleep_ms(1)

def lcd_puts(s):

    l = len(s)
    for i in range(l):
       lcd_putch(s[i])

def lcd_putch(c):

    lcd_write(c, 1)

def lcd_goto(col, row):
    c = col + 1
    if row == 0:
        address = 0
    if row == 1:
        address = 0x40
    if row == 2:
        address = 0x14
    if row == 3:
        address = 0x54
    address = address + c - 1
    lcd_write(0x80 | address, 0)

def lcd_init():
    
    Configure()
    utime.sleep_ms(120)
    for i in range(4):
        L[i].value(0)
    utime.sleep_ms(50)
    L[0].value(1)
    L[1].value(1)
    lcd_strobe()
    utime.sleep_ms(10)
    lcd_strobe()
    utime.sleep_ms(10)
    lcd_strobe()
    utime.sleep_ms(10)
    L[0].value(0)
    lcd_strobe()
    utime.sleep_ms(5)
    lcd_write(0x28, 0)
    utime.sleep_ms(1)
    lcd_write(0x08, 0)
    utime.sleep_ms(1)
    lcd_write(0x01, 0)
    utime.sleep_ms(10)
    lcd_write(0x06, 0)
    utime.sleep_ms(5)
    lcd_write(0x0C, 0)
    utime.sleep_ms(10)
#================= END OF LCD FUNCTIONS =======================


