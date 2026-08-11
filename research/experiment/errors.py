class ExperimentError(Exception):
    """Base exception for experiment engine errors."""
    pass

class ExperimentExecutionError(ExperimentError):
    """Raised when an experiment fails to execute, such as when validation fails."""
    pass
