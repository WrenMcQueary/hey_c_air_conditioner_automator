"""
Low-level classes and functions related to temperature.
"""


def celsius_to_fahrenheit(temperature: float) -> float:
    """Convert a temperature in degrees Celsius to degrees Fahrenheit
    """
    return temperature * 9 / 5 + 32


def resistance_to_voltage(resistance: float) -> float:
    """Given a thermistor resistance value, return the voltage if the thermistor is the top
    half of a voltage divider between 3.3 V and ground.
    """
    v_in = 3.3
    r_other = 10e3
    return v_in * r_other / (resistance + r_other)


class TemperatureResistancePair:
    def __init__(self, temperature, resistance):
        self.temperature = temperature
        self.resistance = resistance


class TemperatureVoltagePair:
    def __init__(self, temperature, voltage):
        self.temperature = temperature
        self.voltage = voltage

    def copy(self):
        return TemperatureVoltagePair(self.temperature, self.voltage)


class TemperatureTable:
    def __init__(self):
        celsius_resistance_pairs = [
            TemperatureResistancePair(0, 31.77E3),
            TemperatureResistancePair(1, 30.25E3),
            TemperatureResistancePair(2, 28.82E3),
            TemperatureResistancePair(3, 27.45E3),
            TemperatureResistancePair(4, 26.16E3),
            TemperatureResistancePair(5, 24.94E3),
            TemperatureResistancePair(6, 23.77E3),
            TemperatureResistancePair(7, 22.67E3),
            TemperatureResistancePair(8, 21.62E3),
            TemperatureResistancePair(9, 20.63E3),
            TemperatureResistancePair(10, 19.68E3),
            TemperatureResistancePair(11, 18.78E3),
            TemperatureResistancePair(12, 17.93E3),
            TemperatureResistancePair(13, 17.12E3),
            TemperatureResistancePair(14, 16.35E3),
            TemperatureResistancePair(15, 15.62E3),
            TemperatureResistancePair(16, 14.93E3),
            TemperatureResistancePair(17, 14.26E3),
            TemperatureResistancePair(18, 13.63E3),
            TemperatureResistancePair(19, 13.04E3),
            TemperatureResistancePair(20, 12.47E3),
            TemperatureResistancePair(21, 11.92E3),
            TemperatureResistancePair(22, 11.41E3),
            TemperatureResistancePair(23, 10.91E3),
            TemperatureResistancePair(24, 10.45E3),
            TemperatureResistancePair(25, 10.00E3),
            TemperatureResistancePair(26, 9.575E3),
            TemperatureResistancePair(27, 9.170E3),
            TemperatureResistancePair(28, 8.784E3),
            TemperatureResistancePair(29, 8.416E3),
            TemperatureResistancePair(30, 8.064E3),
            TemperatureResistancePair(31, 7.730E3),
            TemperatureResistancePair(32, 7.410E3),
            TemperatureResistancePair(33, 7.106E3),
            TemperatureResistancePair(34, 6.815E3),
            TemperatureResistancePair(35, 6.538E3),
            TemperatureResistancePair(36, 6.273E3),
            TemperatureResistancePair(37, 6.020E3),
            TemperatureResistancePair(38, 5.778E3),
            TemperatureResistancePair(39, 5.548E3),
            TemperatureResistancePair(40, 5.327E3),
            TemperatureResistancePair(41, 5.117E3),
            TemperatureResistancePair(42, 4.915E3),
            TemperatureResistancePair(43, 4.723E3),
            TemperatureResistancePair(44, 4.539E3),
            TemperatureResistancePair(45, 4.363E3),
            TemperatureResistancePair(46, 4.195E3),
            TemperatureResistancePair(47, 4.034E3),
            TemperatureResistancePair(48, 3.880E3),
            TemperatureResistancePair(49, 3.733E3),
            TemperatureResistancePair(50, 3.592E3),
            ]
        fahrenheit_resistance_pairs = [TemperatureResistancePair(celsius_to_fahrenheit(item.temperature), item.resistance) for item in celsius_resistance_pairs]
        self.fahrenheit_voltage_pairs = [TemperatureVoltagePair(item.temperature, resistance_to_voltage(item.resistance)) for item in fahrenheit_resistance_pairs]
        # It's important that self.fahrenheit_voltage_pairs monotonically increase in both temperature and voltage

    def voltage_to_temperature(self, voltage: float) -> float:
        """Given a voltage measured at the voltage divider's output, return the
        temperature of the thermistor in degrees Fahrenheit.
        Uses linear interpolation.
        """
        # Handle errors
        # voltage not a float
        if not isinstance(voltage, float) and not isinstance(voltage, int):
            raise TypeError("voltage must be a float or int")

        # Get the datapoint immediately below and above
        highest_point_below = self.fahrenheit_voltage_pairs[0]
        lowest_point_above = self.fahrenheit_voltage_pairs[-1]
        for pair in self.fahrenheit_voltage_pairs:
            if pair.voltage < voltage and pair.voltage > highest_point_below.voltage:
                highest_point_below = pair.copy()
            if pair.voltage > voltage and pair.voltage < lowest_point_above.voltage:
                lowest_point_above = pair.copy()
                break
        # Interpolate and return
        try:
            percent_from_lower_to_upper = (voltage - highest_point_below.voltage) / (lowest_point_above.voltage - highest_point_below.voltage)
        except ZeroDivisionError:   # If the voltage is outside the temperature table
            if voltage < 1.5:
                return -1000
            else:
                return 1000
        return highest_point_below.temperature * (1 - percent_from_lower_to_upper) + lowest_point_above.temperature * (percent_from_lower_to_upper)
