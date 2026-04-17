# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

def imu_accel(readout):
	# Convert from 16 bit unsigned to 16 bit signed
	if readout < 0x8000: 
		signed_int = readout
	else:
		signed_int = readout - 0x10000

	# Convert to acceleration	
	num_bits = 16
	g_setting = 16  # +- 16g
	g = 9.8 # m/s^2
	accel_step = 2 * g_setting * g / float(2**(num_bits) - 1)
	
	return accel_step * signed_int 

def imu_gyro(readout):
	# Convert from 16 bit unsigned to 16 bit signed
	if readout < 0x8000: 
		signed_int = readout
	else:
		signed_int = readout - 0x10000

	# Convert to acceleration	
	num_bits         = 16
	gyro_setting     = 2000.0 # +- 250 deg/s
	gyro_sensitivity = float(2**(num_bits) - 1) / (2 * gyro_setting)  # LSB/(deg/s)
	
	return float(signed_int) / (gyro_sensitivity) 

def baro_press(readout):
	return readout * 0.001

def _adc_to_voltage(readout: int) -> float:
    """Convert a 16-bit ADC readout to a voltage (3.3 V reference).

    :param readout: Raw 16-bit unsigned ADC value.
    :type readout: int
    :returns: Voltage in volts.
    :rtype: float
    """
    return readout * (3.3 / 65536.0)

def pt_pressure(readout: int) -> float:
    """Convert a raw ADC reading from an amplified pressure transducer to psi.

    Uses an instrumentation amplifier with Rref = 100 kΩ and Rgain = 3.3 kΩ
    (gain ≈ 31.3×), and a full-scale transducer output of 0.1 V → 1000 psi.

    :param readout: Raw 16-bit unsigned ADC value.
    :type readout: int
    :returns: Pressure in psi.
    :rtype: float
    """
    voltage = _adc_to_voltage(readout)
    gain = 1.0 + (100.0 / 3.3)
    max_voltage = gain * 0.1
    return voltage * (1000.0 / max_voltage)

def pt_pressure_5V(readout: int) -> float:
    """Convert a raw ADC reading from a 5 V pressure transducer to psi.

    Assumes a linear 0–5 V output corresponding to 0–2000 psi.

    :param readout: Raw 16-bit unsigned ADC value.
    :type readout: int
    :returns: Pressure in psi.
    :rtype: float
    """
    voltage = _adc_to_voltage(readout)
    return voltage * (2000.0 / 5.0)

def tc_temp(readout: int) -> float:
    """Convert a raw thermocouple readout to degrees Celsius.

    The thermocouple IC encodes temperature across two bytes:
    the upper byte carries the integer part (×16) and the lower
    byte carries the fractional part (÷16).  Bit 15 is the sign.

    :param readout: Raw 16-bit thermocouple value (upper byte = integer,
        lower byte = fraction).
    :type readout: int
    :returns: Temperature in °C.
    :rtype: float
    """
    upper_byte = (readout & 0xFF00) >> 8
    lower_byte = readout & 0x00FF
    negative = (upper_byte & 0x80) == 0x80
    temp = float(upper_byte) * 16.0 + float(lower_byte) / 16.0
    if negative:
        temp -= 4096.0
    return temp

def loadcell_force(readout: int) -> float:
    """Convert a raw ADC reading from the load cell to force in lb.

    Uses the same amplifier circuit as :func:`pt_pressure`
    (Rref = 100 kΩ, Rgain = 3.3 kΩ) and assumes a sensitivity of
    1000 lb at 0.1 V pre-amplification.

    :param readout: Raw 16-bit unsigned ADC value.
    :type readout: int
    :returns: Force in lb.
    :rtype: float
    """
    voltage = _adc_to_voltage(readout)
    gain = 1.0 + (100.0 / 3.3)
    return (voltage / gain) * (1000.0 / 0.1)