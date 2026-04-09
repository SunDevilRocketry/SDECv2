from Exception import sdec_error


class ParserError(sdec_error):
    """Exception raised when required parser has error."""
    
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        super().str()