# -----------------------------------------
#                 NOTES 
# -----------------------------------------

# Dieter Steinhauser
# 11/2023

# The Battery we are using is a WEIZE 12V 50Ah LiFePO4, 4 Cells
# Max/Full Charge 14.6V, 3.65V/cell
# Nominal Voltage = 12.8V, 3.2V/cell
# Full Discharge = 10V, 2.50V/Cell
# LiFePO4 Voltage Chart, Best estimated while loaded and not charging.


# 100% Charging - 3.65V/Cell - 14.6V
# 100% Rest     - 3.40/Cell - 13.6V
# 90%           - 3.35/Cell - 13.4V
# 80%           - 3.32/Cell - 13.3V
# 70%           - 3.30/Cell - 13.2V
# 60%           - 3.27/Cell - 13.1V
# 50%           - 3.26/Cell - 13.0V
# 40%           - 3.25/Cell - 13.0V
# 30%           - 3.22/Cell - 12.9V
# 20%           - 3.20/Cell - 12.8V
# 10%           - 3.00/Cell - 12.0V
# 0%            - 2.50/Cell - 10.0V

# STATES

# Battery Full - MPPT Charging - no load    # Waste State -> Performance State
# Battery Full - MPPT Charging - load       # Performance State
# Battery Full - No MPPT - no load          # Energy Saving State, minor tasks
# Battery Full - No MPPT - load             # Performance State, Minor tasks


# Battery mid - MPPT Charging - no load     # Energy Saving State, Recharging
# Battery mid - MPPT Charging - load        # Energy Saving State, Recharging / minor tasks
# Battery mid - No MPPT - no load           # Energy Saving State, Depletion
# Battery mid - No MPPT - load              # Unwanted State, Depletion

# Battery low - MPPT Charging - no load     # Recovery State, Critical Recharging
# Battery low - MPPT Charging - load        # Recovery State, Critical Recharging
# Battery low - no MPPT - no load           # Recovery State, Critical Depletion
# Battery low - no MPPT - load              # Recovery State, Critical Depletion

# -----------------------------------------
#               IMPORTS
# -----------------------------------------

import time

# -----------------------------------------
#           METHODS
# -----------------------------------------
 

class BatteryMonitor:
    """
    Battery Montioring Class, incorporating methods for determining the state of charge.

    The battery monitor must be changed to best fit the chemistry, voltage, and capacity of the
    attached battery.

    The battery monitoring algorithims are derived from the following article for State of Charge (SoC)
    https://www.analog.com/en/technical-articles/a-closer-look-at-state-of-charge-and-state-health-estimation-tech.html

    """

    BATTERY_STATES = {'PERFORMANCE': 0, 'ENERGY_SAVER': 1, 'CRITICAL': 2}

    def __init__ (self, capacity_ah, max_voltage, min_voltage, critical_voltage, critical_percentage, charge_efficiency=1, discharge_efficiency=1):
        """
        Initialization of the battery monitoring system.

        :param capacity_ah: Battery Capacity in Amp Hours
        :type capacity_ah: int | float
        :param max_voltage: Maximum Voltage possible for the battery
        :type max_voltage: int | float
        :param min_voltage: Minimum Voltage possible for the battery
        :type min_voltage: int | float
        :param critical_voltage: Voltage that is deemed the critical point for low power mode.
        :type critical_voltage: int | float
        :param critical_percentage: Percentage that is deemed the critical point for low power mode.
        :type critical_percentage: int | float
        :param charge_efficiency: Efficiency of battery charging, defaults to 1
        :type charge_efficiency: int | float, optional
        :param discharge_efficiency: Efficiency of battery discharging, defaults to 1
        :type discharge_efficiency: int | float, optional
        """
        
        self.capacity_ah = capacity_ah # battery Capacity in amp hours
        self.capacity_mah = 1000 * capacity_ah # battery Capacity in milliamp hours
        self.critical_voltage  = critical_voltage   # Voltage theshold for low battery in volts
        self.critical_percentage  = critical_percentage   # charge percentage threshold for low battery.
        self.max_voltage  = max_voltage  # Maximum voltage of the battery when charging.
        self.min_voltage  = min_voltage  # minimum voltage of the battery when discharging.
        self.charge_percentage = 100
        self.discharge_percentage = 100 - self.charge_percentage
        self.health = 100
        self.depth_of_charge = 0
        self.depth_of_discharge = 0
        self.charge_cycles = 0
        self.discharge_efficiency = discharge_efficiency
        self.charge_efficiency = charge_efficiency
        self.time = time.ticks_ms()
        self.peak_charge_time = time.time()
        self.state = self.BATTERY_STATES.get('ENERGY_SAVER')

    def initial_state_of_charge(self, battery_dict):
        """
        Determines the initial state of charge either from memory or estimation using battery voltage observed.

        :param battery_dict: Dictionary of battery values from the poll_adc_channels() method. 
        :type battery_dict: dict
        """

        # default to the last battery SOC saved to memory
        # TODO: Read memory and determine the last saved state of charge or recall data from the Beelink via UART

        # if none are available, try to estimate the SOC using voltage.

        # parse the battery dictionary
        battery_current = battery_dict.get("IBAT")
        battery_voltage = battery_dict.get("VBAT")
        charge_current = battery_dict.get("ICHARGER")

        # estimate the initial state of charge based on the battery voltage
        # calculated linear regression line of the Discharge chart. 95% confidence, Rsquared = 0.6705 for moderate correlation, voltage = 0.02577(charge) + 11.51.
        charge_percentage = max(0, min(100, ((battery_voltage - 11.51) / 0.02577) ))

        # edit the class variables.
        self.charge_percentage = charge_percentage
        self.discharge_percentage = 100 - self.charge_percentage
        self.time = time.ticks_ms()

            

    def state_of_charge(self, current, time_interval_ms):
        """
        Determines the State of Battery Charge using Coulomb Counting. Requires a recent current reading
        from the battery and a time interval between measurements.

        :param current: Current being supplied to/from the battery. Written in Amps. Charging is negative, Supplying is positive.
        :type current: float
        :param time_interval_ms: Time interval between measurements in milliseconds
        :type time_interval_ms: int | float
        """
        # find the change in charge with respect to time.
        # print(time_interval_ms)
        delta_ah = current * time_interval_ms / 3_600_000
        # print(f'delta Ah: {delta_ah}')

        # find the percentage change in charge
        percent_delta = 100 * (delta_ah / self.capacity_ah)
        # print(f'percent_delta: {percent_delta}')

        # Determine difference between charging and discharging efficiency.
        efficiency = self.discharge_efficiency if current > 0 else self.charge_efficiency

        # TODO: Determine if providing a minimum and maximum charging range here makes sense for DOD.
        # print(f'discharge_percentage: {self.discharge_percentage}')
        self.discharge_percentage = max(0, min(100, self.discharge_percentage + (efficiency * percent_delta)))
        # self.discharge_percentage = self.discharge_percentage + (efficiency * percent_delta)
        # print(f'discharge_percentage: {self.discharge_percentage}')

        # Calculate the State of charge percentage based on the battery health and the discharge percentage.
        self.charge_percentage = max(0, min(100, (self.health - self.discharge_percentage)))


    def monitor_battery(self, battery_dict):
        """
        Method for monitoring a batteries state of charge using ADC readings and Coulomb counting.

        :param battery_dict: Dictionary of battery values from the poll_adc_channels() method.
        :type battery_dict: dict
        :return: State of charge percentage, battery health percentage, and power state.
        :rtype: tuple
        """

        # parse the battery dictionary
        battery_current = battery_dict.get("IBAT")
        battery_voltage = battery_dict.get("VBAT")
        charge_current = battery_dict.get("ICHARGER")

        # print(f'battery current: {battery_current}')
        # print(f'Charger current: {charge_current}')
        # #print(charge_current)

        # find the time since the last time the battery monitored function was called.
        new_time = time.ticks_ms()
        time_elapsed = time.ticks_diff(new_time, self.time)
        self.time = new_time
        # scalar being multiplied to reflect the 0.25V:1A ratio
        battery_current = ((battery_current - 2.5) * 4)
        charge_current = max(0, charge_current * 4)

        # print(f'battery current adjusted: {battery_current}')
        # print(f'Charger current adjusted: {charge_current}')
        # print(f'time elapsed: {time_elapsed}')

        # If the battery is charging
        if battery_current < 0:
            
            # TODO Measure the smallest accepted current by the battery and change the charge current threshold accordingly.
            # if the battery is fully charged, with max voltage achieved and charge current less than 50mA
            if (battery_voltage >= self.max_voltage) and (-0.050 < battery_current < 0):
                
                # if it has been more than 5 minutes since the last peak charge trigger
                if self.peak_charge_time == 0 or ((time.time() - self.peak_charge_time) >= 300):
                
                    # Increment the amount of charge cycles that have occured
                    self.charge_cycles += 1

                # if this is the first time that we have fully charged the battery, calibrate the SoC system.
                if self.charge_cycles == 1:

                    # The Battery is fully charged, calibrate the system to reflect 
                    self.discharge_percentage = 0
                    self.charge_percentage = 100

                # Set the battery health to the state of charge
                self.health = self.charge_percentage

            else:
                # calculate the state of charge and depth of discharge
                self.state_of_charge(battery_current, time_elapsed)

            # if the battery is at or above the healthy top of the charge or sees large charging current, allow for performance mode.
            if(self.charge_percentage >= self.health) or (self.charge_percentage > 70 and charge_current > 2):
                self.state = self.BATTERY_STATES.get('PERFORMANCE')

        # if the battery is discharging
        else:

            # if the battery is lower than the discharged battery voltage
            if battery_voltage <= self.min_voltage:

                # if it has been more than 5 minutes since the last peak charge trigger
                if self.peak_charge_time == 0 or ((time.time() - self.peak_charge_time) >= 300):
                
                    # Increment the amount of charge cycles that have occured
                    self.charge_cycles += 1

                # if this is the first time that we have fully charged the battery, calibrate the SoC system.
                if self.charge_cycles == 1:

                    # The Battery is fully discharged, calibrate the system to reflect this.
                    self.discharge_percentage = 100
                    self.charge_percentage = 0


                # Set the battery health to the depth of discharge
                self.health = self.discharge_percentage

            else:
                # calculate the state of charge and depth of discharge
                self.state_of_charge(battery_current, time_elapsed)


            # Handle states of low/critical power.
            if (battery_voltage <= self.critical_voltage) or (self.charge_percentage <= self.critical_percentage):
                self.state = self.BATTERY_STATES.get('CRITICAL')

            else:
                self.state = self.BATTERY_STATES.get('ENERGY_SAVER')

        # write significant data to the flash.
        # TODO Impelement Flash reading and writing or recalling data from the Beelink via UART

        # return battery data for UART transmission.
        bat_monitor_dict = {}
        bat_monitor_dict['CHARGE'] = self.charge_percentage
        bat_monitor_dict['HEALTH'] = self.health
        bat_monitor_dict['STATE'] = self.state

        return bat_monitor_dict
    
if __name__ == '__main__':

    bm = BatteryMonitor(capacity_ah = 50,
                        max_voltage = 14.4,
                        min_voltage = 10.2,
                        critical_voltage = 12.8, 
                        critical_percentage= 20, 
                        charge_efficiency=1, 
                        discharge_efficiency=1 )
    



# -----------------------------------------
#         END OF FILE
# -----------------------------------------  

