from .sdec_error import SDECError

class ComportError(SDECError):
    """Exception raised when using a Comport incorrectly."""
    
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"