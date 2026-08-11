from dataclasses import dataclass, field
from types import MappingProxyType
import math
from research.splitting.errors import InvalidSplitConfigurationError

@dataclass(frozen=True)
class SplitConfig:
    train_ratio: float
    validation_ratio: float
    test_ratio: float
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self):
        if self.train_ratio < 0 or self.validation_ratio < 0 or self.test_ratio < 0:
            raise InvalidSplitConfigurationError("All ratios must be >= 0.")
        
        total = self.train_ratio + self.validation_ratio + self.test_ratio
        if not math.isclose(total, 1.0, abs_tol=1e-7):
            raise InvalidSplitConfigurationError(f"Sum of ratios must equal 1.0, got {total}")
