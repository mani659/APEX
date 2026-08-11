from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Tuple, Optional
from enum import Enum

class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

@dataclass(frozen=True)
class ValidationIssue:
    severity: Severity
    category: str
    message: str
    record_index: Optional[int] = None
    feature_name: Optional[str] = None
    label_name: Optional[str] = None
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

@dataclass(frozen=True)
class ValidationReport:
    valid: bool
    issue_count: int
    error_count: int
    warning_count: int
    issues: Tuple[ValidationIssue, ...]
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
