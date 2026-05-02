from .sdec_error import SDECError

class SerialError(SDECError):
    """Exception raised when a Serial operation fails"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"