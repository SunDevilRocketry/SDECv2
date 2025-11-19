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