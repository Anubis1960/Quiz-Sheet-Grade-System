class StringLengthError(Exception):
    """Exception raised when input string exceed maximum length."""
    def __init__(self, message="String exceeds the maximum allowed length"):
        super().__init__(message)