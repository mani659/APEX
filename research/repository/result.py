from dataclasses import dataclass, field
from types import MappingProxyType
from research.experiment.result import ExperimentRecord

@dataclass(frozen=True)
class RepositoryEntry:
    experiment_id: str
    created_timestamp: str
    experiment_record: ExperimentRecord
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
