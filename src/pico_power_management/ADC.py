# -----------------------------------------
#                 NOTES 
# -----------------------------------------

# Dieter Steinhauser
# 11/2023

# ADC Polling

# Drone Maestros Power Management and Measurement Pico. Controls DC/DC converters over I2C, 
# Measures Rail outputs, Measure battery Charging/Discharging, and Solar output.

# -----------------------------------------
#               IMPORTS
# -----------------------------------------
import time
from machine import ADC, Pin, Timer
import gc


# -----------------------------------------
#           CONSTANTS
# -----------------------------------------

UPY_BIT_RES = 16
ADC_REF = 3
VOLT_PER_BIT = ADC_REF / (2**UPY_BIT_RES) # ADC recieves in 2 byte packets and micropython automagically fixes it.


# -----------------------------------------
#            ADC
# -----------------------------------------
adc0 = ADC(26) # Connect to GP26, which is channel 0
adc1 = ADC(27) # Connect to GP27, which is channel 1
adc2 = ADC(28) # Connect to GP28, which is channel 2
# adc_reading = adc0.read_u16() * VOLT_PER_BIT # read and report the ADC reading


# -----------------------------------------
#           GPIO
# -----------------------------------------

# Mux Switches
# ----------------------------
sw0 = Pin(18, Pin.OUT, value=0)
sw1 = Pin(19, Pin.OUT, value=0)
sw2 = Pin(20, Pin.OUT, value=0)
sw3 = Pin(21, Pin.OUT, value=0)
switch_pins = [sw0, sw1, sw2, sw3]

mux_toggle_pin = Pin(22, Pin.OUT, value=0)
mux_toggle = 0

# -----------------------------------------
#          METHODS
# ----------------------------------------- 

ADC_OFFSET = 0 # 0.020 # Volts
CURR_OFFSET = 0.050 # Volts



# Voltage scalars are applied because of voltage dividers conditioning the readings for the 0-3V ADC.
# NOTE An error in the hardware design creates a thevinin equivalent circuit. These values are scaled in such a way to counteract this issue.
# Theoretical scalar * thevinin scalar * error adjust
VADJ_SCALAR = 10.999 * 1.012           # Theoretical: 10.999, 1.2 thevinin loading
V20_SCALAR = 10.999  * 1.012          # Theoretical: 10.999, 1.2 thevinin loading
V12_SCALAR = 8.021  * 1          # Theoretical: 8.021, 1.414 thevinin loading
V5_SCALAR = 3.34 * 1          # Theoretical: 3.34, 1.329 thevinin loading
voltage_scalars = [VADJ_SCALAR, V20_SCALAR, V12_SCALAR, V5_SCALAR]
# voltage_scalars = [1, 1, 1, 1]

# current scalars are applied because of voltage dividers conditioning the readings for the 0-3V ADC.
IADJ_SCALAR = 1.5
I20_SCALAR = 1.5
I12_SCALAR = 1.5
I5_SCALAR = 1.5
current_scalars = [IADJ_SCALAR, I20_SCALAR, I12_SCALAR, I5_SCALAR]
# current_scalars = [1, 1, 1, 1]

# Voltage and current scalars are applied because of voltage dividers conditioning the readings for the 0-3V ADC.
# NOTE An error in the hardware design creates a thevinin equivalent circuit. These values are scaled in such a way to counteract this issue.
VBAT_SCALAR = 8.021 * 1.02  # Theoretical scalar * error adjust
IBAT_SCALAR =  1.5 * 1.4229 # * 4 scalar being multiplied to reflect the 0.25V:1A ratio, must occur after subtraction
ICHARGER_SCALAR = 1.5 * 1  # * 4 scalar being multiplied to reflect the 0.25V:1A ratio, must occur after subtraction
MISC_SCALAR = 1
mux3_scalars = [VBAT_SCALAR, IBAT_SCALAR, ICHARGER_SCALAR, MISC_SCALAR]


# Offsets are applied to remove analog offsets in the system
VBAT_OFFSET = 0
IBAT_OFFSET = 0 # 2.5 offset is expected, however sending negative numbers over UART proved troublesome.
ICHARGER_OFFSET = CURR_OFFSET # CURR_OFFSET
MISC_OFFSET = 0
mux3_offsets = [VBAT_OFFSET, IBAT_OFFSET, ICHARGER_OFFSET, MISC_OFFSET]

# TODO Implement mux4 offset as the MUX becomes populated
M1_OFFSET = 0
M2_OFFSET = 0
M3_OFFSET = 0 
M4_OFFSET = 0
mux4_offsets = [M1_OFFSET, M2_OFFSET, M3_OFFSET, M4_OFFSET]

# TODO Implement mux4 scalars as the MUX becomes populated
M1_SCALAR = 1
M2_SCALAR = 1
M3_SCALAR = 1
M4_SCALAR = 1
mux4_scalars = [M1_SCALAR, M2_SCALAR, M3_SCALAR, M4_SCALAR]


def poll_adc_channels():
    """
    Perform a conversion on each ADC channel for each GPIO Switch channel.

    The function iterates through the switch pins (GPIO18-21) that controls the attached Analog multiplexer IC's. 
    For each active switch, an ADC can take a reading and store the data. We perform this to fill 12 readings.

    Every time the method is called, GPIO22 is toggled so that we swap between mux3 and mux4 of the Analog multiplexer IC's.
    This alternating means that one of the four returned data structures will be empty as a result.

    :return: Returns four Dictionaries, one for each group of multiplexer readings.
    :rtype: tuple(dict)
    """
    global mux_toggle
    global ADC_OFFSET
    global CURR_OFFSET
    global voltage_scalars
    global current_scalars
    global mux3_scalars
    global mux3_offsets
    global mux4_scalars
    global mux4_offsets

    # Set the timeout function to be called after the specified duration
    #timeout_timer.init(mode=Timer.ONE_SHOT, period=5000, callback=timeout_handler)

    voltage_dict = {}
    current_dict = {}
    mux3_dict = {}
    mux4_dict = {}


    mux_1_order = ['ADJ', '20V', '12V', '5V']
    mux_2_order = ['ADJ', '20V', '12V', '5V']
    mux_3_order = ["VBAT", "IBAT", "ICHARGER", "MISC"]
    mux_4_order = ["M1", "M2", "M3", "M4"]


    
    # Iterate through the Mux Switches 
    for index in range(4):
        
        # Set the desired GPIO high while others are low. Read each ADC channel.
        switch_pins[index].value(1)

        # Pico Setup and Hold Time is 2us, 20us is stable in python.
        # time.sleep_us(20)
        adc0_reading = (adc0.read_u16() * VOLT_PER_BIT) # Voltage Measurements
        time.sleep_us(2)
        adc1_reading = (adc1.read_u16() * VOLT_PER_BIT) # Current Measurements
        time.sleep_us(2)
        adc2_reading = (adc2.read_u16() * VOLT_PER_BIT) # Misc Measurements
        time.sleep_us(2)

        # Set the GPIO low after reading channels.
        switch_pins[index].value(0)
        
        # store the data based on measurement taken and the appropriate math required.
        # Round the ADC reading with ADC hardware offsets removed. Value should be at least zero. Scale and offset to match actual value.
        # Data is stored in corresponding dictionary with an appropriate name.

        voltage_dict[mux_1_order[index]] = (max(0, (round(adc0_reading, 3) ) ) * voltage_scalars[index])
        current_dict[mux_2_order[index]] = (max(0, (round(adc1_reading - ADC_OFFSET, 3) ) ) * current_scalars[index]) - CURR_OFFSET

        if mux_toggle == 1:
            mux3_dict[mux_3_order[index]] = max(0, round(adc2_reading - ADC_OFFSET, 3)) * mux3_scalars[index] - mux3_offsets[index]
        else: 
            mux4_dict[mux_4_order[index]] = max(0, round(adc2_reading - ADC_OFFSET, 3)) * mux4_scalars[index] - mux4_offsets[index]
    
    # Toggle the Mux Pin and garbage collect.
    mux_toggle_pin.toggle()
    mux_toggle = not mux_toggle
    gc.collect()

    return  voltage_dict, current_dict, mux3_dict, mux4_dict    

# -----------------------------------------
#               END OF FILE
# ----------------------------------------- 
