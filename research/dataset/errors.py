class DatasetError(Exception):
    """Base exception for all dataset-related errors."""
    pass

class DatasetAlignmentError(DatasetError):
    """Raised when FeatureStore and LabelStore lengths or timestamps do not strictly align."""
    pass

class DuplicateColumnError(DatasetError):
    """Raised when feature names or label names collide."""
    pass
