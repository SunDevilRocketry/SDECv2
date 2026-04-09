from .sdec_error import SDECError


class MissingDataError(SDECError):
    """Exception raised when required data is missing."""
    
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
       return super().__str__()