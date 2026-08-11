class ValidationError(Exception):
    """Base exception for validation engine errors."""
    pass

class DatasetValidationError(ValidationError):
    """Raised when the validation engine itself fails to execute properly."""
    pass
