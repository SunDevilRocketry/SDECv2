from .sdec_error import SDECError


class InvalidDataError(SDECError):
    """Exception raised when required data is invalid."""
    
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return super().__str__()