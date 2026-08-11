class AnalysisError(Exception):
    """Base exception for analysis engine errors."""
    pass

class FeatureAnalysisError(AnalysisError):
    """Raised when feature analysis encounters an execution failure."""
    pass
