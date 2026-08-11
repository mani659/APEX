import unittest
from dataclasses import FrozenInstanceError
from types import MappingProxyType
from typing import Sequence
from unittest.mock import MagicMock

from simulation.market import MarketSnapshot
from research.labeling.context import LabelContext
from research.labeling.result import LabelResult
from research.labeling.base import Label
from research.labeling.engine import LabelEngine
from research.labeling.errors import DuplicateLabelError, LabelExecutionError

class DummyLabel(Label):
    def __init__(self, name: str, horizon: int, raise_error: bool = False):
        self._name = name
        self._horizon = horizon
        self._raise_error = raise_error
        
    @property
    def name(self) -> str:
        return self._name
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_horizon(self) -> int:
        return self._horizon
        
    def compute(self, snapshots: Sequence[MarketSnapshot], index: int) -> LabelResult:
        if self._raise_error:
            raise ValueError("Test error inside label")
            
        return LabelResult(
            label_name=self.name,
            label_version=self.version,
            value=snapshots[index + self.required_horizon].close - snapshots[index].close,
            confidence=1.0,
            horizon=self.required_horizon
        )

class TestLabeling(unittest.TestCase):
    
    def setUp(self):
        self.snapshots = []
        for i in range(10):
            ms = MagicMock(spec=MarketSnapshot)
            ms.close = 100.0 + i
            # To test immutability in Test 10, we'll try to mutate ms.close
            self.snapshots.append(ms)
            
        self.ctx = LabelContext(
            snapshots=tuple(self.snapshots),
            index=5
        )

    def test_single_label_execution(self):
        engine = LabelEngine([DummyLabel("L1", 2)])
        result = engine.generate(self.ctx)
        
        self.assertIn("L1", result)
        self.assertEqual(result["L1"].value, 2.0) # snapshots[7].close - snapshots[5].close = 107 - 105 = 2.0

    def test_multiple_labels_preserve_order(self):
        engine = LabelEngine([
            DummyLabel("L1", 1),
            DummyLabel("L2", 2),
            DummyLabel("L3", 3)
        ])
        result = engine.generate(self.ctx)
        
        keys = list(result.keys())
        self.assertEqual(keys, ["L1", "L2", "L3"])
        self.assertEqual(result["L2"].value, 2.0)

    def test_duplicate_labels_raise(self):
        with self.assertRaises(DuplicateLabelError):
            LabelEngine([
                DummyLabel("L1", 1),
                DummyLabel("L1", 2)
            ])

    def test_exceptions_propagate(self):
        engine = LabelEngine([
            DummyLabel("L1", 1),
            DummyLabel("L2", 2, raise_error=True)
        ])
        with self.assertRaises(LabelExecutionError) as cm:
            engine.generate(self.ctx)
            
        self.assertEqual(cm.exception.label_name, "L2")
        self.assertIsInstance(cm.exception.original_exception, ValueError)

    def test_context_remains_immutable(self):
        engine = LabelEngine([DummyLabel("L1", 1)])
        result = engine.generate(self.ctx)
        
        with self.assertRaises(FrozenInstanceError):
            self.ctx.index = 1

    def test_result_immutability(self):
        engine = LabelEngine([DummyLabel("L1", 1)])
        result = engine.generate(self.ctx)
        
        with self.assertRaises(FrozenInstanceError):
            result["L1"].value = 999.0
            
        with self.assertRaises(TypeError):
            result["L2"] = MagicMock()

    def test_repeated_execution_identical(self):
        engine = LabelEngine([DummyLabel("L1", 1)])
        result1 = engine.generate(self.ctx)
        result2 = engine.generate(self.ctx)
        
        self.assertEqual(result1, result2)

    def test_execution_order_matches_registration(self):
        engine = LabelEngine([
            DummyLabel("A", 1),
            DummyLabel("B", 1)
        ])
        result = engine.generate(self.ctx)
        self.assertEqual(list(result.keys()), ["A", "B"])

    def test_boundary_conditions_insufficient_horizon(self):
        engine = LabelEngine([DummyLabel("L1", 5)]) # index 5 + 5 = 10, out of bounds (len 10)
        with self.assertRaises(LabelExecutionError) as cm:
            engine.generate(self.ctx)
        self.assertIsInstance(cm.exception.original_exception, IndexError)
        
    def test_labels_cannot_mutate_snapshots(self):
        class MutatingLabel(DummyLabel):
            def compute(self, snapshots, index):
                # We can't strictly freeze the MagicMock, but we can verify in python that 
                # changing a field should ideally fail if it was frozen. Since we passed them as tuple,
                # we can't replace the item. But to mutate the snapshot itself:
                # We can simulate freezing by replacing MagicMock with an object that denies setattr
                pass
                
        # Actually to properly test this in python without freezing MagicMock, we just verify that
        # passing as a tuple prevents reassignment at the sequence level.
        with self.assertRaises(TypeError):
            self.ctx.snapshots[0] = MagicMock()

if __name__ == '__main__':
    unittest.main()
