class LabelError(Exception):
    """Base exception for all labeling-related errors."""
    pass

class DuplicateLabelError(LabelError):
    """Raised when duplicate label names are registered in the LabelEngine."""
    pass

class LabelExecutionError(LabelError):
    """Raised when a label fails to compute (e.g., due to insufficient horizon or mathematical faults)."""
    def __init__(self, label_name: str, original_exception: Exception):
        super().__init__(f"Label '{label_name}' failed to compute: {str(original_exception)}")
        self.label_name = label_name
        self.original_exception = original_exception
