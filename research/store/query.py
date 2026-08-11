from typing import Sequence
from research.pipeline.result import PipelineResult
from research.store.store import FeatureStore
from research.store.errors import FeatureNotFoundError

def get_range(store: FeatureStore, start: float, end: float) -> Sequence[PipelineResult]:
    """
    Returns all PipelineResult objects chronologically between start and end timestamps (inclusive).
    """
    all_results = store.get_all()
    # Linear scan is sufficient for an in-memory, simple implementation without indexes
    return tuple(r for r in all_results if start <= r.timestamp <= end)

def first(store: FeatureStore) -> PipelineResult:
    """
    Returns the chronologically first PipelineResult in the store.
    """
    if len(store) == 0:
        raise FeatureNotFoundError("The Feature Store is empty.")
    return store.get_all()[0]

def last(store: FeatureStore) -> PipelineResult:
    """
    Returns the chronologically last PipelineResult in the store.
    """
    if len(store) == 0:
        raise FeatureNotFoundError("The Feature Store is empty.")
    return store.get_all()[-1]
