from .sdec_error import SDECError


class ParserError(SDECError):
    """Exception raised when required parser has error."""
    
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"