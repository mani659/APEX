from typing import Dict, Sequence, Tuple
from research.pipeline.result import PipelineResult
from research.store.errors import DuplicateTimestampError, FeatureNotFoundError

class FeatureStore:
    """
    Immutable in-memory repository of computed feature vectors.
    Stores and retrieves PipelineResult objects sequentially.
    """
    
    def __init__(self):
        self._store: Dict[float, PipelineResult] = {}
        
    def add(self, result: PipelineResult) -> None:
        """
        Stores a PipelineResult. Rejects duplicate timestamps.
        """
        if result.timestamp in self._store:
            raise DuplicateTimestampError(f"Timestamp {result.timestamp} already exists in the Feature Store.")
        self._store[result.timestamp] = result
        
    def get(self, timestamp: float) -> PipelineResult:
        """
        Retrieves a PipelineResult by timestamp.
        """
        if timestamp not in self._store:
            raise FeatureNotFoundError(f"No feature vector found for timestamp {timestamp}.")
        return self._store[timestamp]
        
    def get_all(self) -> Sequence[PipelineResult]:
        """
        Returns all stored PipelineResults in chronological order as an immutable collection.
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
        Returns the number of stored PipelineResults.
        """
        return len(self._store)
