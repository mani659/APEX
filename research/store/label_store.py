from dataclasses import dataclass, field
from typing import Dict, Sequence
from types import MappingProxyType
from research.labeling.result import LabelResult
from research.store.errors import DuplicateTimestampError, FeatureNotFoundError

@dataclass(frozen=True)
class LabelStoreResult:
    """
    Immutable standard output object for labels mapped to a timestamp.
    """
    timestamp: float
    label_results: MappingProxyType[str, LabelResult]
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

class LabelStore:
    """
    Immutable in-memory repository of computed label vectors.
    Stores and retrieves LabelStoreResult objects sequentially.
    """
    
    def __init__(self):
        self._store: Dict[float, LabelStoreResult] = {}
        
    def add(self, result: LabelStoreResult) -> None:
        """
        Stores a LabelStoreResult. Rejects duplicate timestamps.
        """
        if result.timestamp in self._store:
            raise DuplicateTimestampError(f"Timestamp {result.timestamp} already exists in the Label Store.")
        self._store[result.timestamp] = result
        
    def get(self, timestamp: float) -> LabelStoreResult:
        """
        Retrieves a LabelStoreResult by timestamp.
        """
        if timestamp not in self._store:
            raise FeatureNotFoundError(f"No label vector found for timestamp {timestamp}.")
        return self._store[timestamp]
        
    def get_all(self) -> Sequence[LabelStoreResult]:
        """
        Returns all stored LabelStoreResults in chronological order as an immutable collection.
        """
        sorted_keys = sorted(self._store.keys())
        return tuple(self._store[k] for k in sorted_keys)
        
    def clear(self) -> None:
        """
        Clears all entries from the store.
        """
        self._store.clear()
        
    def __len__(self) -> int:
        """
        Returns the number of stored LabelStoreResults.
        """
        return len(self._store)
