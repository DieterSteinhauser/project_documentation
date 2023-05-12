# -----------------------------------------
#          NOTES 
# -----------------------------------------
"""

Dieter Steinhauser
11/2022
Design 1
SPI configuration

The following is configuration of SPI communication for the LTC1661 10-bit DAC.
"""

# -----------------------------------------
#          IMPORTS
# -----------------------------------------
from machine import Pin, SPI

# -----------------------------------------
#          CONSTANTS
# -----------------------------------------
DEBUG_SPI_CLK = 1_000_000 # Hz
STABLE_SPI_CLK = 8_000_000 # Hz
FAST_SPI_CLK = 10_000_000 # Hz
IDLE_LO = 0
IDLE_HI = 1
RISING_EDGE = 0
FALLING_EDGE = 1

# -----------------------------------------
#           SPI
# -----------------------------------------

# Note: How to configure SPI
# ---------------------------
# spi.init(baudrate=1_000_000,  # clock speed
         # polarity=0,          # Idle clock level. 0:L, 1:H
         # phase=0,             # sample on rising(0) or falling (1) edge
         # bits=8,              # width of transfer in bits, 8 is standard
         # firstbit=SPI.MSB,    # bit order, either SPI.MSB or SPI.LSB
         # sck=None,            # alternate pin object selection 
         # mosi=None,           # alternate pin object selection 
         # miso=None,           # alternate pin object selection 
         # pins=(SCK, MOSI, MISO) # alternate pin object selection for WiPy
         # )

# spi.write('test') # single write to the device
# spi.read(num_bytes)       # read a number of bytes. can take a second parameter of a continuous write byte value.
# 
# buf = bytearray(3)
# spi.write_readinto('out', read_buf) # writes the first value while reading into the second parameter read_buf
# ---------------------------

spi_clock_speed = FAST_SPI_CLK
spi = SPI(0)
# Default Pins for SPI-0
# CLK  - 18
# MOSI - 19
# MISO - 16
# CS   - 17 #Note, if this does not work immeadiately, enable the pin as an output as seen below. 

cs = Pin(17, Pin.OUT, value=1)

spi.init(baudrate=spi_clock_speed,  # clock speed
         polarity=IDLE_LO,    # Idle clock level. 0:L, 1:H
         phase=RISING_EDGE,    # sample on rising(0) or falling (1) edge
         )
