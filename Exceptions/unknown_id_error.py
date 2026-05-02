from .sdec_error import SDECError

class UnknownIdError(SDECError):
    """Exception raised when an unknown Hardware/Firmware ID is used."""
    
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"