from typing import Sequence
from types import MappingProxyType
from research.labeling.base import Label
from research.labeling.context import LabelContext
from research.labeling.result import LabelResult
from research.labeling.errors import DuplicateLabelError, LabelExecutionError

class LabelEngine:
    """
    Executes registered labels sequentially for a given context.
    No ML, statistics, or caching.
    """
    
    def __init__(self, labels: Sequence[Label]):
        self._validate_unique_names(labels)
        self._labels = tuple(labels)
        
    def _validate_unique_names(self, labels: Sequence[Label]) -> None:
        seen = set()
        for lbl in labels:
            if lbl.name in seen:
                raise DuplicateLabelError(f"Duplicate label name detected: '{lbl.name}'")
            seen.add(lbl.name)
            
    def generate(self, context: LabelContext) -> MappingProxyType[str, LabelResult]:
        """
        Executes all labels exactly once in registration order.
        Raises LabelExecutionError if a label fails (e.g. out of bounds).
        """
        results = {}
        
        for lbl in self._labels:
            if context.index + lbl.required_horizon >= len(context.snapshots):
                ex = IndexError(f"Insufficient future data for label '{lbl.name}' requiring horizon {lbl.required_horizon}")
                raise LabelExecutionError(lbl.name, ex) from ex
                
            try:
                results[lbl.name] = lbl.compute(context.snapshots, context.index)
            except Exception as ex:
                raise LabelExecutionError(lbl.name, ex) from ex
                
        return MappingProxyType(results)
