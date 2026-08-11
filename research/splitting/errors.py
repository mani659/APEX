class SplitError(Exception):
    """Base exception for splitting engine errors."""
    pass

class InvalidSplitConfigurationError(SplitError):
    """Raised when the split configuration is invalid (e.g. ratios don't sum to 1.0)."""
    pass
