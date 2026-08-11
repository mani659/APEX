class RepositoryError(Exception):
    """Base exception for repository errors."""
    pass

class DuplicateExperimentError(RepositoryError):
    """Raised when attempting to overwrite an existing experiment without permission."""
    pass
    
class RepositoryReadError(RepositoryError):
    """Raised when an experiment fails to load."""
    pass
    
class RepositoryWriteError(RepositoryError):
    """Raised when an experiment fails to save."""
    pass
