from dataclasses import dataclass, field
from types import MappingProxyType
from research.splitting.config import SplitConfig

@dataclass(frozen=True)
class ExperimentConfig:
    experiment_name: str
    experiment_version: str
    split_config: SplitConfig
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
