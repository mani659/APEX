from dataclasses import dataclass, field
from types import MappingProxyType

@dataclass(frozen=True)
class RepositoryConfig:
    repository_path: str
    overwrite_existing: bool = False
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))
