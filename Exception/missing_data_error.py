from Exception import sdec_error
#for imu, baro, servo, config, and bitmask data


class MissingDataError(sdec_error):
    """Exception raised when required data is missing."""
    
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        super().str()