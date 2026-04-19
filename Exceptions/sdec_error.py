class SDECError(Exception):
    """Base class for exceptions in SDEC."""
    
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"SDECError: {self.message}"