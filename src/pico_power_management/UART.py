# -----------------------------------------
#                 NOTES 
# -----------------------------------------

# Ryan Laur
# Dieter Steinhauser
# 11/2023

# UART Helpers

# Drone Maestros Power Management and Measurement Pico. Controls DC/DC converters over I2C, 
# Measures Rail outputs, Measure battery Charging/Discharging, and Solar output.



# -----------------------------------------
#               IMPORTS
# -----------------------------------------
import time


# -----------------------------------------
#               METHODS
# -----------------------------------------

def send_uart_data(uart, id_value, value):
    """
    Sends data over UART. ID first, followed by value.

    :param uart: UART communication object
    :type uart: uart
    :param id_value: ID for the type of data.
    :type id_value: int
    :param value: The data value.
    :type value: float | int
    """

    value = int(value * 1000)
    #print(value)

    # Convert ID and value to bytes and send
    #uart.write(id_value.to_bytes(1, 'big'))
    #uart.write(value.to_bytes(2, 'big'))
    combined_bytes = id_value.to_bytes(1, 'big') + value.to_bytes(2, 'big')
    # Convert ID and value to bytes and send
    uart.write(combined_bytes)
    time.sleep_ms(40)



def tx_rail_data(uart, mux1 = None, mux2 = None, mux3 = None, mux4 = None):
    """
    Sends voltage and current values for each rail over UART.

    :param uart: UART communication object
    :type uart: uart
    :param mux1: Data from the voltage mux, corresponds to the output rails.
    :type mux1: dict
    :param mux2: Data from the current mux, corresponds to the output rails. 
    :type mux2: dict
    :param mux3: Data from the battery measurement mux. Contains both current and voltage data.
    :type mux3: dict
    :param mux4: Data from the expansion measurement mux. Data TBD
    :type mux4: dict
    """
    # Mux keys for user reference. Not needed in code.
    # mux_1 = ['ADJ', '20V', '12V', '5V']
    # mux_2 = ['ADJ', '20V', '12V', '5V']
    # mux_3 = ["VBAT", "IBAT", "ICHARGER", "MISC"]
    # mux_4 = ["M1", "M2", "M3", "M4"]

    base_id = 1
    mux_set = [mux1, mux2, mux3, mux4]

    # 4*index + (index+1) 

    for mux in mux_set: # iterate through each dictionary.

        # if a mux was passed in and not empty, iterate through the mux.
        if mux is not None and len(mux) > 0:
            mux_index = mux_set.index(mux)
            read_index = 0

            for value in mux.values(): # Iterate through each value, send the data and index the base ID.
                
                # formulate the base ID based on the mux sent and the iteration through the mux.
                read_index += 1
                base_id = (4 * mux_index) + read_index

                # Send the UART Data
                send_uart_data(uart, base_id, value) 


def tx_bms_data(uart, bms_dict):
    """
    Sends battery monitor values over UART

    :param uart: UART communication object
    :type uart: uart
    :param bms_dict: Data from the Battery management system
    :type bms_dict: dict
    """
    # BMS keys for user reference. Not needed in code.
    # bat_monitor_dict['CHARGE'] = self.charge_percentage
    # bat_monitor_dict['HEALTH'] = self.health
    # bat_monitor_dict['STATE'] = self.state

    base_id = 69 # Unique ID from the Rail data sent.

    for value in bms_dict.values(): # Iterate through each value, send the data and index the base ID.

        if (base_id==69):
            value = value / 1000
            
        print(str(value))
        # Send the UART Data
        send_uart_data(uart, base_id, value)
        base_id +=1
        # increment the base ID

# -----------------------------------------
#               END OF FILE
# -----------------------------------------