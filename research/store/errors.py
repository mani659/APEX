class FeatureStoreError(Exception):
    """Base exception for all Feature Store related errors."""
    pass

class DuplicateTimestampError(FeatureStoreError):
    """Raised when attempting to add a PipelineResult with a timestamp that already exists."""
    pass

class FeatureNotFoundError(FeatureStoreError):
    """Raised when requesting a PipelineResult by a timestamp that does not exist."""
    pass
