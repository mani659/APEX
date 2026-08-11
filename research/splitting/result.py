from dataclasses import dataclass, field
from types import MappingProxyType
from research.dataset.result import Dataset
from research.splitting.config import SplitConfig

@dataclass(frozen=True)
class DatasetSplit:
    train_dataset: Dataset
    validation_dataset: Dataset
    test_dataset: Dataset
    configuration: SplitConfig
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
