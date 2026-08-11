class PipelineError(Exception):
    """Base exception for all pipeline-related errors."""
    pass

class DuplicateFeatureError(PipelineError):
    """Raised when duplicate feature names are detected during pipeline construction."""
    pass

class FeatureExecutionError(PipelineError):
    """Raised when a feature throws an exception during pipeline execution."""
    def __init__(self, feature_name: str, original_exception: Exception):
        super().__init__(f"Feature '{feature_name}' failed to execute: {str(original_exception)}")
        self.feature_name = feature_name
        self.original_exception = original_exception
