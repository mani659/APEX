import unittest
from dataclasses import FrozenInstanceError
from types import MappingProxyType
from typing import FrozenSet
from unittest.mock import MagicMock

from simulation.market import MarketSnapshot
from simulation.context import TradingContext
from research.features.context import FeatureContext
from research.features.result import FeatureResult
from research.features.base import Feature
from research.pipeline.pipeline import FeaturePipeline
from research.pipeline.errors import DuplicateFeatureError, FeatureExecutionError
from research.pipeline.result import PipelineResult

class DummyFeature(Feature):
    def __init__(self, name: str, value: float, raise_error: bool = False):
        self._name = name
        self._value = value
        self._raise_error = raise_error
        
    @property
    def name(self) -> str:
        return self._name
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset()
        
    def compute(self, context: FeatureContext) -> FeatureResult:
        if self._raise_error:
            raise ValueError("Test error inside feature")
        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=self._value,
            confidence=0.9
        )

class TestPipeline(unittest.TestCase):
    
    def setUp(self):
        self.market_mock = MagicMock(spec=MarketSnapshot)
        self.market_mock.timestamp = 1625097600.0
        self.context_mock = MagicMock(spec=TradingContext)
        self.ctx = FeatureContext(
            market_snapshot=self.market_mock,
            trading_context=self.context_mock
        )

    def test_pipeline_executes_one_feature(self):
        pipeline = FeaturePipeline([DummyFeature("A", 10.0)])
        result = pipeline.run(self.ctx)
        
        self.assertEqual(result.timestamp, 1625097600.0)
        self.assertIn("A", result.feature_results)
        self.assertEqual(result.feature_results["A"].value, 10.0)

    def test_pipeline_executes_multiple_in_order(self):
        pipeline = FeaturePipeline([
            DummyFeature("A", 10.0),
            DummyFeature("B", 20.0),
            DummyFeature("C", 30.0)
        ])
        result = pipeline.run(self.ctx)
        
        keys = list(result.feature_results.keys())
        self.assertEqual(keys, ["A", "B", "C"])
        self.assertEqual(result.feature_results["B"].value, 20.0)

    def test_duplicate_names_raise_on_init(self):
        with self.assertRaises(DuplicateFeatureError):
            FeaturePipeline([
                DummyFeature("A", 10.0),
                DummyFeature("A", 20.0)
            ])

    def test_feature_exception_propagates(self):
        pipeline = FeaturePipeline([
            DummyFeature("A", 10.0),
            DummyFeature("B", 20.0, raise_error=True)
        ])
        
        with self.assertRaises(FeatureExecutionError) as cm:
            pipeline.run(self.ctx)
            
        self.assertEqual(cm.exception.feature_name, "B")
        self.assertIsInstance(cm.exception.original_exception, ValueError)

    def test_feature_context_unchanged(self):
        # We know FeatureContext is immutable, but we can verify it runs without mutating anything we pass
        pipeline = FeaturePipeline([DummyFeature("A", 10.0)])
        result = pipeline.run(self.ctx)
        self.assertEqual(self.ctx.market_snapshot.timestamp, 1625097600.0)

    def test_pipeline_result_immutable(self):
        pipeline = FeaturePipeline([DummyFeature("A", 10.0)])
        result = pipeline.run(self.ctx)
        
        with self.assertRaises(FrozenInstanceError):
            result.timestamp = 1.0
            
        with self.assertRaises(TypeError):
            result.feature_results["new"] = MagicMock()

    def test_repeated_runs_identical(self):
        pipeline = FeaturePipeline([DummyFeature("A", 10.0)])
        result1 = pipeline.run(self.ctx)
        result2 = pipeline.run(self.ctx)
        
        self.assertEqual(result1, result2)

    def test_one_feature_cannot_mutate_another_output(self):
        pipeline = FeaturePipeline([DummyFeature("A", 10.0)])
        result = pipeline.run(self.ctx)
        
        with self.assertRaises(FrozenInstanceError):
            result.feature_results["A"].confidence = 1.0

if __name__ == '__main__':
    unittest.main()
