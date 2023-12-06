# -----------------------------------------
#                 NOTES 
# -----------------------------------------
"""
Dieter Steinhauser
10/2023

PowerPico

Drone Maestros Power Management and Measurement Pico. Controls DC/DC converters over I2C, 
Measures Rail outputs, Measure battery Charging/Discharging, and Solar output.

"""

# -----------------------------------------
#               IMPORTS
# -----------------------------------------

# from LCD import LCD
# import _thread
import time
from machine import Pin, Timer, ADC, freq, I2C, UART, WDT
import gc
from TPS55288 import TPS55288
from TCA9548 import TCA9548
from DRV8871 import DRV8871
from UART import tx_rail_data, tx_bms_data
from SERIAL import tx_serial_rail_data, tx_serial_bms_data
from battery_monitor import BatteryMonitor
from ADC import * # needs to be all so we can have the pins and such that are assigned here.
import sys

# -----------------------------------------
#         CONSTANTS/VARIABLES
# -----------------------------------------   

# ------------------

DEBUG = False # Debug output on/off
I2C_EN = True # I2C Communication at the start of system.
WATCHDOG_EN = False # Watchdog timer usage

# ------------------

REFRESH_RATE = 5 # Frequency in Hz
REFRESH_PERIOD = int((1 / REFRESH_RATE) * 1000) # delay in milliseconds


# -------------------------------------------------------------
#           INITIALIZATION
# -------------------------------------------------------------

# -----------------------------------------
#           SYSTEM CLOCK
# -----------------------------------------

DEFAULT_SYS_CLK = 125_000_000
STABLE_OVERCLOCK = 270_000_000
UNDERCLOCK = 270_000_000

# Pico can go up to 270MHz before needing to flash to the eeprom directly.
system_clock = UNDERCLOCK

# if the system clock is not the default, apply the clock speed.
if system_clock !=  DEFAULT_SYS_CLK:
    freq(system_clock)

# print(f'Clock: {freq()/1e6}MHz')

# -----------------------------------------
#               PINOUT
# -----------------------------------------

    """

  _______________________________________________________________________________________  
  |     Variable/Pin     |    Pin    |  Pin  |  Pin  |    Pin    |     Variable/Pin     |
  |       Name/Use       |   Label   |  Num  |  Num  |   Label   |       Name/Use       |
  |                      |           |       |       |           |                      |
  |______________________|___________|_______|_______|___________|_______________ ___ __|
  |                      |   GP0     |   1   |  40   |   VBUS    |    USB 5V Supply     |
  |                      |   GP1     |   2   |  39   |   VSYS    |  Filter/Protect 5V   |
  |      Ground Ref      |   GND     |   3   |  38   |   GND     |      Ground Ref      |
  |                      |   GP2     |   4   |  37   |   3V3_EN  | WPU,SC GND ->3v3 OFF |
  |                      |   GP3     |   5   |  36   |   3V3_OUT | 3.3V out from DC/DC  |
  |                      |   GP4     |   6   |  35   |   ADC_REF |    ADC ref pin       |
  |                      |   GP5     |   7   |  34   |   GP28    |    ADC2 Channel      |
  |      Ground Ref      |   GND     |   8   |  33   |   GND     |    ADC Ground Ref    |
  |                      |   GP6     |   9   |  32   |   GP27    |    ADC1 Channel      |
  |                      |   GP7     |  10   |  31   |   GP26    |    ADC0 Channel      |
  |       UART TX        |   GP8     |  11   |  30   |   RUN     | WPU, SC->GND to RST  |
  |       UART RX        |   GP9     |  12   |  29   |   GP22    |   ADC Muxing Switch  |
  |      Ground Ref      |   GND     |  13   |  28   |   GND     |      Ground Ref      |
  |   CHARGE_ORIENT_1    |   GP10    |  14   |  27   |   GP21    |      Mux CTRL D      |
  |   CHARGE_ORIENT_2    |   GP11    |  15   |  26   |   GP20    |      Mux CTRL C      |
  |   H-BRIDGE IN2       |   GP12    |  16   |  25   |   GP19    |      Mux CTRL B      |
  |   H-BRIDGE IN1       |   GP13    |  17   |  24   |   GP18    |      Mux CTRL A      |
  |    Ground Ref        |   GND     |  18   |  23   |   GND     |      Ground Ref      |
  |  I2C Serial Data     |   GP14    |  19   |  22   |   GP17    |                      |
  |  I2C Serial Clock    |   GP15    |  20   |  21   |   GP16    |                      |
  |______________________|___________|_______|_______|___________|______________________|

"""

# LEDs
# ----------------------------
led_onboard = Pin("LED", Pin.OUT)

# -----------------------------------------
#            I2C Devices
# -----------------------------------------

# TODO Implement I2C switch to swap between channels and cut down on I2C busses.
# TODO In final development use hardware settings to change I2C address.

i2c_bus =  I2C(1, sda=Pin(14), scl=Pin(15, Pin.OUT), freq=100_000)

if I2C_EN:

    # create the TCA9548 Device to swap between TPS Devices
    tca_switch = TCA9548(name="TCA9548", address=0x70, i2c_bus=i2c_bus)

    # if debugging, print the addresses of connected I2C Devices.
    if DEBUG:
        devices = i2c_bus.scan()
        hex_addr = [hex(x) for x in devices]
        print(f"Seen device addresses: {hex_addr}")


    # Startup Sequence
    # -------------------

    # Set the 12V channel on for door motors and such
    tca_switch.enable_channel(0)
    tps_12V = TPS55288('12V Rail', 0x74, i2c_bus=i2c_bus)
    tps_12V.voltage(12)
    tps_12V.output_enable(1)
    
    # if Debugging, Relay the current status of the Device
    if DEBUG:
        print(f"12V rail Voltage setting: {tps_12V.voltage()}")
        print(f"12V rail output setting: {tps_12V.output_enable()}")

    # turn off the channel
    tca_switch.disable_channel(0)

    # Set the 20V channel on so the Beelink may startup.
    tca_switch.enable_channel(1)
    tps_20V = TPS55288('20V Rail', 0x74, i2c_bus=i2c_bus)
    tps_20V.voltage(19) # The beelink likes 19V, just matching the DC/DC that it comes with...
    tps_20V.output_enable(1)
    
    # if Debugging, Relay the current status of the Device
    if DEBUG:
        print(f"20V rail Voltage setting: {tps_20V.voltage()}")
        print(f"20V rail output setting: {tps_20V.output_enable()}")

    # turn off the channel
    tca_switch.disable_channel(1)

    # Set the VADJ channel on so we may start charging the drone battery.
    tca_switch.enable_channel(2)
    tps_VADJ = TPS55288('Adjustable Charging Rail', 0x74, i2c_bus=i2c_bus)
    tps_VADJ.voltage(9) # This voltage can change as needed by the drone battery being charged
    tps_VADJ.output_enable(1)
    
    # if Debugging, Relay the current status of the Device
    if DEBUG:
        print(f"VADJ rail Voltage setting: {tps_VADJ.voltage()}")
        print(f"VADJ rail output setting: {tps_VADJ.output_enable()}")

    # turn off the channel
    tca_switch.disable_channel(2)


# -----------------------------------------
#        Drone Battery Charging Circuit
# -----------------------------------------

a_amber_orient = Pin(10, Pin.IN)
b_blue_orient = Pin(11, Pin.IN)
charger_drv = DRV8871(name='Motor Driver', in1 = Pin(13, Pin.OUT), in2=Pin(12, Pin.OUT))

ORIENTATION_TIMEOUT = 30 # 30 seconds seems good for field but lower for debug
if DEBUG:
    ORIENTATION_TIMEOUT = 2
charger_timer = time.time()

def charger_orientation():
    """
    Determines how the H-bridge should charge the drone, if at all.
    
    :return: Returns the status of the H-bridge.
    :rtype: dict
    """
    global charger_timer

    
    # read the values from the device
    a = a_amber_orient.value()
    b = b_blue_orient.value()

    # see how long it has been since we have checked orientation without H-bridge on
    if (time.time() - charger_timer) >= ORIENTATION_TIMEOUT:
        
        # turn off the H-bridge to see if voltage still exists, this indicates if the drone is present or flying.
        charger_drv.brake()
        time.sleep_ms(100)

        # reset the charger timer
        charger_timer = time.time()

    if a == 0 and b == 0:

        # tell the charger to disable when nothing is connected.
        charger_drv.brake()
        status = charger_drv.status()

    elif a == 1 and b == 0:
        
        # tell the charger to put itself in the forward state 

        # This is a debug line, and should be full forward in final implementation
        charger_drv.forward(duty = 20, coast=False)
        # charger_drv.full_forward() 

        status = charger_drv.status()

    elif a == 0 and b == 1:
    
        # tell the charger to put itself in the backward state 

        # This is a debug line, and should be full backward in final implementation
        charger_drv.backward(duty = 20, coast=False)
        # charger_drv.full_backward()
        status =charger_drv.status()
    
    else:
        # if for whatever reason we end up here, stop charging.
        charger_drv.brake()
        status = charger_drv.status()

    return status
# -----------------------------------------
#           ADC
# -----------------------------------------
# adc0 = ADC(26) # Connect to GP26, which is channel 0
# adc1 = ADC(27) # Connect to GP27, which is channel 1
# adc2 = ADC(28) # Connect to GP28, which is channel 2
# adc_reading = adc0.read_u16() * VOLT_PER_BIT # read and report the ADC reading


# -----------------------------------------
#           WATCHDOG TIMER
# -----------------------------------------

# enable the WDT with a timeout of 5s (1s is the minimum)
if WATCHDOG_EN:
    wdt = WDT(timeout=5000)
    wdt.feed()

# -----------------------------------------
#           UART
# -----------------------------------------

# Initialize UART
uart = UART(1, baudrate=115200, tx=Pin(8, Pin.OUT), rx=Pin(9, Pin.IN), bits=8, parity=2, stop=0)


# -----------------------------------------
#           BATTERY MONITOR
# -----------------------------------------

bm = BatteryMonitor(capacity_ah = 9,
                    max_voltage = 14.4,
                    min_voltage = 10.2,
                    critical_voltage = 12.8, 
                    critical_percentage= 20, 
                    charge_efficiency=1, 
                    discharge_efficiency=1 )


# -----------------------------------------
#           METHODS
# -----------------------------------------


# -----------------------------------------
#           PROCESS 1: IO
# -----------------------------------------

startup = True

if startup is True:
    led_onboard(1)
    time.sleep(1)
    led_onboard.toggle()

# Poll the ADC channels until we recieve Battery data for the initial setup.
battery_mux = {}
while len(battery_mux) == 0:
    _, _, battery_mux, _ = poll_adc_channels()

bm.initial_state_of_charge(battery_mux)
print(f'Battery Charge: {bm.charge_percentage}%') if DEBUG else None # what a beautiful one-liner!
time.sleep(1)




while True:
    
    # Poll the ADC for data
    voltage, current, battery_mux, mux4 = poll_adc_channels()
    


    if DEBUG:
        # tx_rail_data(uart, mux1 = voltage, mux2 = current, mux3 = battery_mux, mux4=None)
        # TODO Remove print debugging here when implementing system

        print(f'voltage {voltage}    ') 
        print(f'current {current}    ') 
        print()
        print()


        if mux_toggle_pin.value() == 0: # Note that the mux toggle pin got flipped at the end of the poll adc function.
 
            print(f'Battery {battery_mux}    ')
            print(f'Battery Monitor {bm.monitor_battery(battery_mux)}    ')
            print()
            print()



        else:
            pass
            # print(f'Expansion {mux4}')

                # If there is battery data, update the battery monitor
        if len(battery_mux) > 0:
            tx_bms_data(uart, bm.monitor_battery(battery_mux))
    else:
        #print(f'Battery {battery_mux}    ')
        tx_serial_rail_data(sys, mux1 = voltage, mux2 = current, mux3 = battery_mux, mux4=None)
        if len(battery_mux) > 0:
            tx_serial_bms_data(sys, bm.monitor_battery(battery_mux))
        
    #value = 1;
    #sys.stdout.buffer.write(value.to_bytes(1, 'big'))
    #value = 5000;
    #sys.stdout.buffer.write(value.to_bytes(2, 'big'))
    # toggle onboard LED for System speed status and refresh delay
    # -----------------------------------------
    led_onboard.toggle()
    charger_orientation()
    time.sleep_ms(REFRESH_PERIOD)
    # wdt.feed()
    gc.collect()
    




