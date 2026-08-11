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
from research.features.feature_set import FeatureSet
from research.features.registry import FeatureRegistry

class DummyFeature(Feature):
    @property
    def name(self) -> str:
        return "dummy_feature"
        
    @property
    def version(self) -> str:
        return "1.0"
        
    @property
    def required_inputs(self) -> FrozenSet[str]:
        return frozenset(["market_snapshot"])
        
    def compute(self, context: FeatureContext) -> FeatureResult:
        return FeatureResult(
            feature_name=self.name,
            feature_version=self.version,
            value=42.0,
            confidence=0.9,
            metadata=MappingProxyType({"test": "data"})
        )

class TestFeatures(unittest.TestCase):
    
    def setUp(self):
        self.market_mock = MagicMock(spec=MarketSnapshot)
        self.context_mock = MagicMock(spec=TradingContext)
        self.ctx = FeatureContext(
            market_snapshot=self.market_mock,
            trading_context=self.context_mock
        )

    def test_feature_result_immutable(self):
        result = FeatureResult(
            feature_name="test",
            feature_version="1",
            value=100.0,
            confidence=None,
            metadata=MappingProxyType({"key": "val"})
        )
        with self.assertRaises(FrozenInstanceError):
            result.value = 200.0
            
        with self.assertRaises(TypeError):
            result.metadata["key"] = "new_val"

    def test_feature_context_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            self.ctx.indicator_cache = MappingProxyType({})
            
        with self.assertRaises(TypeError):
            self.ctx.indicator_cache["new_key"] = "val"

    def test_dummy_feature_computes(self):
        feature = DummyFeature()
        result = feature.compute(self.ctx)
        self.assertEqual(result.value, 42.0)
        self.assertEqual(result.confidence, 0.9)
        self.assertEqual(result.metadata["test"], "data")

    def test_feature_set_orchestrates(self):
        features = FeatureSet([DummyFeature()])
        results = features.compute(self.ctx)
        self.assertIn("dummy_feature", results)
        self.assertEqual(results["dummy_feature"].value, 42.0)

    def test_registry_registers_and_retrieves(self):
        registry = FeatureRegistry()
        feature = DummyFeature()
        registry.register(feature)
        
        retrieved = registry.get("dummy_feature")
        self.assertEqual(retrieved.name, "dummy_feature")
        self.assertIn("dummy_feature", registry.list_features())
        
    def test_registry_refuses_duplicates(self):
        registry = FeatureRegistry()
        feature1 = DummyFeature()
        feature2 = DummyFeature()
        registry.register(feature1)
        
        with self.assertRaises(ValueError):
            registry.register(feature2)
            
    def test_determinism_guarantee(self):
        feature = DummyFeature()
        result1 = feature.compute(self.ctx)
        result2 = feature.compute(self.ctx)
        result3 = feature.compute(self.ctx)
        
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)

if __name__ == '__main__':
    unittest.main()
