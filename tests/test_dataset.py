import unittest
from dataclasses import FrozenInstanceError
from types import MappingProxyType
from unittest.mock import MagicMock

from research.features.result import FeatureResult
from research.pipeline.result import PipelineResult
from research.store.store import FeatureStore
from research.labeling.result import LabelResult
from research.store.label_store import LabelStore, LabelStoreResult
from research.dataset.builder import build_dataset
from research.dataset.errors import DatasetAlignmentError, DuplicateColumnError
from research.dataset.result import Dataset, DatasetRecord

class TestDatasetBuilder(unittest.TestCase):
    
    def setUp(self):
        self.f_store = FeatureStore()
        self.l_store = LabelStore()
        
        # Mocks for values
        f1 = FeatureResult(feature_name="f1", feature_version="1", value=10.0, confidence=1.0)
        f2 = FeatureResult(feature_name="f2", feature_version="1", value=20.0, confidence=1.0)
        
        l1 = LabelResult(label_name="l1", label_version="1", value=1.0, confidence=1.0, horizon=1)
        l2 = LabelResult(label_name="l2", label_version="1", value=0.0, confidence=1.0, horizon=1)

        self.pr1 = PipelineResult(timestamp=100.0, feature_results=MappingProxyType({"f1": f1, "f2": f2}))
        self.pr2 = PipelineResult(timestamp=200.0, feature_results=MappingProxyType({"f1": f1}))
        
        self.lr1 = LabelStoreResult(timestamp=100.0, label_results=MappingProxyType({"l1": l1, "l2": l2}))
        self.lr2 = LabelStoreResult(timestamp=200.0, label_results=MappingProxyType({"l1": l1}))

    def test_single_aligned_record(self):
        self.f_store.add(self.pr1)
        self.l_store.add(self.lr1)
        
        dataset = build_dataset(self.f_store, self.l_store)
        self.assertEqual(len(dataset.records), 1)
        
        r0 = dataset.records[0]
        self.assertEqual(r0.timestamp, 100.0)
        self.assertEqual(r0.features["f1"], 10.0)
        self.assertEqual(r0.features["f2"], 20.0)
        self.assertEqual(r0.labels["l1"], 1.0)

    def test_multiple_aligned_records(self):
        self.f_store.add(self.pr1)
        self.l_store.add(self.lr1)
        self.f_store.add(self.pr2)
        self.l_store.add(self.lr2)
        
        dataset = build_dataset(self.f_store, self.l_store)
        self.assertEqual(len(dataset.records), 2)
        self.assertEqual(dataset.records[0].timestamp, 100.0)
        self.assertEqual(dataset.records[1].timestamp, 200.0)
        
        self.assertIn("f2", dataset.feature_names)
        self.assertIn("l1", dataset.label_names)

    def test_timestamp_mismatch_raises(self):
        self.f_store.add(self.pr1)
        # Mismatch timestamp in label store
        lr_bad = LabelStoreResult(timestamp=101.0, label_results=MappingProxyType({}))
        self.l_store.add(lr_bad)
        
        with self.assertRaises(DatasetAlignmentError):
            build_dataset(self.f_store, self.l_store)

    def test_length_mismatch_raises(self):
        self.f_store.add(self.pr1)
        self.f_store.add(self.pr2)
        self.l_store.add(self.lr1)
        
        with self.assertRaises(DatasetAlignmentError):
            build_dataset(self.f_store, self.l_store)

    def test_duplicate_feature_and_label_names_rejected(self):
        # Setup collision where label is named 'f1'
        l_coll = LabelResult(label_name="f1", label_version="1", value=0.0, confidence=1.0, horizon=1)
        lr_coll = LabelStoreResult(timestamp=100.0, label_results=MappingProxyType({"f1": l_coll}))
        
        self.f_store.add(self.pr1) # Contains 'f1'
        self.l_store.add(lr_coll) # Contains 'f1'
        
        with self.assertRaises(DuplicateColumnError):
            build_dataset(self.f_store, self.l_store)

    def test_dataset_immutability(self):
        self.f_store.add(self.pr1)
        self.l_store.add(self.lr1)
        dataset = build_dataset(self.f_store, self.l_store)
        
        with self.assertRaises(FrozenInstanceError):
            dataset.records = ()
            
        with self.assertRaises(FrozenInstanceError):
            dataset.records[0].timestamp = 999.0
            
        with self.assertRaises(TypeError):
            dataset.records[0].features["f1"] = 0.0

    def test_repeated_builds_identical(self):
        self.f_store.add(self.pr1)
        self.l_store.add(self.lr1)
        
        d1 = build_dataset(self.f_store, self.l_store)
        d2 = build_dataset(self.f_store, self.l_store)
        
        self.assertEqual(d1, d2)

    def test_large_dataset_construction(self):
        # 10,000 records
        for i in range(10000):
            t = float(i)
            self.f_store.add(PipelineResult(timestamp=t, feature_results=MappingProxyType({})))
            self.l_store.add(LabelStoreResult(timestamp=t, label_results=MappingProxyType({})))
            
        dataset = build_dataset(self.f_store, self.l_store)
        self.assertEqual(len(dataset.records), 10000)
        self.assertEqual(dataset.records[-1].timestamp, 9999.0)

if __name__ == '__main__':
    unittest.main()
