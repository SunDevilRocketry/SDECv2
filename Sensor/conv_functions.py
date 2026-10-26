# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Sun Devil Rocketry

"""
This module contains the conversion functions for sensors to use.
Conversion functions are created here then referenced when creating a sensor object.
"""

import math


ISA_PRESSURE_SEA_LEVEL = 101325.0  # Pa
ISA_EXP = 0.190294958
ISA_TEMP_LAPSE_RATE = 0.0065  # K/m
ISA_TROPOPAUSE_PRES = 22632.06  # Pa
ISA_TROPOPAUSE_ALT = 11000.0  # m
ISA_STRATO_SCALE_H = 6341.62  # m
KELVIN_OFFSET = 273.15


def isa_get_altitude_qnh(baro_pres: float, baro_temp: float) -> float:
	"""Calculate ISA altitude above sea level from pressure (Pa) and temperature (°C).

	This mirrors the flight computer's QNH calculation, including its
	troposphere/stratosphere branch at the tropopause pressure. A non-positive
	pressure returns ``math.inf`` to match the firmware's ``INFINITY`` result.
	"""
	if baro_pres <= 0.0:
		return math.inf

	if baro_pres < ISA_TROPOPAUSE_PRES:
		return ISA_TROPOPAUSE_ALT + ISA_STRATO_SCALE_H * math.log(
			ISA_TROPOPAUSE_PRES / baro_pres
		)

	return (
		(math.pow(ISA_PRESSURE_SEA_LEVEL / baro_pres, ISA_EXP) - 1.0)
		* (baro_temp + KELVIN_OFFSET)
		/ ISA_TEMP_LAPSE_RATE
	)


def mach_number(velocity_m_s: float, altitude_m: float) -> float:
	"""Calculate Mach number from velocity (m/s) and altitude above sea level (m).

	The local speed of sound uses the ISA tropospheric temperature lapse rate,
	with temperature held at the tropopause value above 11 km. Velocity may be
	signed; Mach number is returned as a non-negative magnitude.
	"""
	if not math.isfinite(velocity_m_s) or not math.isfinite(altitude_m):
		raise ValueError("Velocity and altitude must be finite values")

	temperature_k = max(216.65, ( KELVIN_OFFSET + 15.0 ) - ISA_TEMP_LAPSE_RATE * altitude_m)
	speed_of_sound = math.sqrt(1.4 * 287.05 * temperature_k)
	return abs(velocity_m_s) / speed_of_sound


def eul_to_quat(yaw: float, pitch: float, roll: float) -> tuple[float, float, float, float]:
	"""Convert ZYX Euler angles in radians to a ``(w, x, y, z)`` quaternion.

	The rotation order is yaw about Z, pitch about Y, then roll about X,
	matching the standard aerospace ZYX convention.
	"""
	cos_yaw = math.cos(yaw / 2.0)
	cos_pitch = math.cos(pitch / 2.0)
	cos_roll = math.cos(roll / 2.0)
	sin_yaw = math.sin(yaw / 2.0)
	sin_pitch = math.sin(pitch / 2.0)
	sin_roll = math.sin(roll / 2.0)

	return (
		cos_roll * cos_pitch * cos_yaw + sin_roll * sin_pitch * sin_yaw,
		sin_roll * cos_pitch * cos_yaw - cos_roll * sin_pitch * sin_yaw,
		cos_roll * sin_pitch * cos_yaw + sin_roll * cos_pitch * sin_yaw,
		cos_roll * cos_pitch * sin_yaw - sin_roll * sin_pitch * cos_yaw,
	)


def quat_to_eul(
	w: float,
	x: float,
	y: float,
	z: float,
) -> tuple[float, float, float]:
	"""Convert a ``(w, x, y, z)`` quaternion to ZYX Euler angles in radians.

	Returns ``(yaw, pitch, roll)`` for rotations about Z, Y, and X respectively,
	matching :func:`eul_to_quat`. The pitch result is clamped to the valid
	``asin`` domain to tolerate small floating-point errors. At gimbal lock,
	roll is set to zero because yaw and roll are not independently recoverable.
	"""
	norm = math.sqrt(w * w + x * x + y * y + z * z)
	if norm <= 1e-12:
		raise ValueError("Cannot convert a zero-magnitude quaternion to Euler angles")

	w, x, y, z = w / norm, x / norm, y / norm, z / norm

	sinp = 2.0 * (w * y - z * x)
	if abs(sinp) >= 1.0 - 1e-12:
		pitch = math.copysign(math.pi / 2.0, sinp)
		singular_yaw = 2.0 * math.atan2(z, w) if sinp > 0.0 else 2.0 * math.atan2(x, w)
		yaw = math.atan2(math.sin(singular_yaw), math.cos(singular_yaw))
		return yaw, pitch, 0.0

	pitch = math.asin(sinp)
	sinr_cosp = 2.0 * (w * x + y * z)
	cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
	roll = math.atan2(sinr_cosp, cosr_cosp)

	siny_cosp = 2.0 * (w * z + x * y)
	cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
	yaw = math.atan2(siny_cosp, cosy_cosp)

	return yaw, pitch, roll

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