# -----------------------------------------
#                 NOTES 
# -----------------------------------------
"""
Dieter Steinhauser
10/2023
TPS55288 I2C Driver

"""

# -----------------------------------------
#               IMPORTS
# -----------------------------------------

from machine import Pin, I2C
import time
from TPS55288 import TPS55288

# -----------------------------------------
#               MAIN
# -----------------------------------------

i2c_bus =  I2C(1, sda=Pin(14), scl=Pin(15), freq=100_000)

if __name__ == '__main__':
    tps =  TPS55288(name="TPS_rail", address=0x74, i2c_bus=i2c_bus)
    devices = tps.i2c_bus.scan()
    hex_addr = [hex(x) for x in devices]
    print(f"Seen device addresses: {hex_addr}")

    test_reading = True
    if test_reading:
        print("Testing reading of each register")
        print("----------------------------------")
        print(bin(tps.VREF_LOW.read()))
        print(bin(tps.VREF_HIGH.read()))
        print(bin(tps.IOUT_LIMIT.read()))
        print(bin(tps.VOUT_SR.read()))
        print(bin(tps.VOUT_FS.read()))
        print(bin(tps.CDC.read()))
        print(bin(tps.MODE.read()))
        print(bin(tps.STATUS.read()))
        print("")

        print("Testing the reading of each field")
        print("----------------------------------")

        print(bin(tps.VREF_LOW.REF_LSB.read()))
        print("")
        print(bin(tps.VREF_HIGH.REF_MSB.read()))
        print("")
        print(bin(tps.IOUT_LIMIT.CURR_LIMIT.read()))
        print(bin(tps.IOUT_LIMIT.CURR_LIMIT_EN.read()))
        print("")
        print(bin(tps.VOUT_SR.SR.read()))
        print(bin(tps.VOUT_SR.OCP_DELAY.read()))
        print("")
        print(bin(tps.VOUT_FS.INTFB.read()))
        print(bin(tps.VOUT_FS.FB.read()))
        print("")
        print(bin(tps.CDC.CDC.read()))
        print(bin(tps.CDC.CDC_OPTION.read()))
        print(bin(tps.CDC.OVP_MASK.read()))
        print(bin(tps.CDC.OCP_MASK.read()))
        print(bin(tps.CDC.SC_MASK.read()))
        print("")
        print(bin(tps.MODE.MODE.read()))
        print(bin(tps.MODE.PFM.read()))
        print(bin(tps.MODE.I2CADD.read()))
        print(bin(tps.MODE.VCC.read()))
        print(bin(tps.MODE.DISCHG.read()))
        print(bin(tps.MODE.HICCUP.read()))
        print(bin(tps.MODE.FSWDBL.read()))
        print(bin(tps.MODE.OE.read()))
        print("")
        print(bin(tps.STATUS.read()))

        print("")  
        print("Reading and Writing the Reference Voltage")
        print("----------------------------------")

        print("")
        print((tps.reference_voltage()))
        time.sleep(0.1)
            
        print("")
        tps.reference_voltage(0.3)
        print('setting reference voltage')
        time.sleep(0.1)
        
            
        print("")
        print((tps.reference_voltage()))
        time.sleep(0.1)
        
        tps.reference_voltage(0.282)
        time.sleep(0.1)
        
        print("")
        print((tps.reference_voltage()))
        time.sleep(0.1)
        
        print("")
        print((tps.status()))
        time.sleep(0.1)

    test_output = True
    if test_output:
        
        # 5V output
        tps.voltage(5)
        print((tps.voltage()))
        time.sleep(1)
        
        print("")
        print((tps.reference_voltage()))
        time.sleep(0.1)
        
        print("")  
        print("Enabling the Output")
        tps.output_enable(value=1)
        print(tps.output_enable())
        
        # 20V output
        tps.voltage(20)
        time.sleep(0.1)
        print((tps.voltage()))
        time.sleep(1)
        
        # 19V output
        tps.voltage(19)
        print((tps.voltage()))
        time.sleep(1)
        
        # 12V output
        tps.voltage(11.9)
        print((tps.voltage()))
        time.sleep(1)
        
        # 9V output
        tps.voltage(9)
        print((tps.voltage()))
        time.sleep(1)

        # 5V output
        tps.voltage(5)
        print((tps.voltage()))
        time.sleep(1)

        # 3.3V output
        tps.voltage(3.24)
        print((tps.voltage()))
        time.sleep(1)
        
        time.sleep(5)
        tps.output_enable(value=0)
        print(tps.output_enable())

    
    i2c_swap = False
    if i2c_swap:
        
        print("Swapping I2C addresses")
        print("----------------------------------")       
        print(tps.mode())
        tps.mode(mode=1, i2c_addr=1)
        print(tps.mode())
        devices = tps.i2c_bus.scan()
        hex_addr = [hex(x) for x in devices]
        print(f"Seen device addresses: {hex_addr}")
        tps =  TPS55288(name="TPS_rail", address=0x75, i2c_bus=i2c_bus)
        print(tps.mode())
    
# -----------------------------------------
#              END OF FILE
# -----------------------------------------