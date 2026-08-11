import unittest
from types import MappingProxyType
from dataclasses import FrozenInstanceError

from research.dataset.result import Dataset, DatasetRecord
from research.splitting.config import SplitConfig
from research.splitting.result import DatasetSplit
from research.splitting.engine import split
from research.splitting.errors import InvalidSplitConfigurationError

class TestSplitEngine(unittest.TestCase):
    
    def setUp(self):
        records = []
        for i in range(100):
            records.append(
                DatasetRecord(
                    timestamp=float(i),
                    features=MappingProxyType({"f1": float(i)}),
                    labels=MappingProxyType({"l1": 1.0})
                )
            )
        self.dataset = Dataset(
            records=tuple(records),
            feature_names=frozenset({"f1"}),
            label_names=frozenset({"l1"}),
            metadata=MappingProxyType({"version": "1.0"})
        )
        self.config = SplitConfig(train_ratio=0.6, validation_ratio=0.2, test_ratio=0.2)

    def test_1_basic_chronological_split(self):
        res = split(self.dataset, self.config)
        self.assertEqual(len(res.train_dataset.records), 60)
        self.assertEqual(len(res.validation_dataset.records), 20)
        self.assertEqual(len(res.test_dataset.records), 20)
        
        self.assertEqual(res.train_dataset.records[0].timestamp, 0.0)
        self.assertEqual(res.train_dataset.records[-1].timestamp, 59.0)
        self.assertEqual(res.validation_dataset.records[0].timestamp, 60.0)
        self.assertEqual(res.validation_dataset.records[-1].timestamp, 79.0)
        self.assertEqual(res.test_dataset.records[0].timestamp, 80.0)
        self.assertEqual(res.test_dataset.records[-1].timestamp, 99.0)

    def test_2_100_percent_training_split(self):
        cfg = SplitConfig(train_ratio=1.0, validation_ratio=0.0, test_ratio=0.0)
        res = split(self.dataset, cfg)
        self.assertEqual(len(res.train_dataset.records), 100)
        self.assertEqual(len(res.validation_dataset.records), 0)
        self.assertEqual(len(res.test_dataset.records), 0)

    def test_3_invalid_ratio_totals(self):
        with self.assertRaises(InvalidSplitConfigurationError):
            SplitConfig(train_ratio=0.5, validation_ratio=0.2, test_ratio=0.2)
            
        with self.assertRaises(InvalidSplitConfigurationError):
            SplitConfig(train_ratio=0.5, validation_ratio=0.5, test_ratio=0.1)
            
        with self.assertRaises(InvalidSplitConfigurationError):
            SplitConfig(train_ratio=-0.1, validation_ratio=0.6, test_ratio=0.5)

    def test_4_temporal_ordering_preserved(self):
        res = split(self.dataset, self.config)
        
        for i in range(1, len(res.train_dataset.records)):
            self.assertTrue(res.train_dataset.records[i].timestamp > res.train_dataset.records[i-1].timestamp)
            
        for i in range(1, len(res.validation_dataset.records)):
            self.assertTrue(res.validation_dataset.records[i].timestamp > res.validation_dataset.records[i-1].timestamp)
            
        for i in range(1, len(res.test_dataset.records)):
            self.assertTrue(res.test_dataset.records[i].timestamp > res.test_dataset.records[i-1].timestamp)

    def test_5_no_overlapping_records(self):
        res = split(self.dataset, self.config)
        train_ts = {r.timestamp for r in res.train_dataset.records}
        val_ts = {r.timestamp for r in res.validation_dataset.records}
        test_ts = {r.timestamp for r in res.test_dataset.records}
        
        self.assertTrue(train_ts.isdisjoint(val_ts))
        self.assertTrue(train_ts.isdisjoint(test_ts))
        self.assertTrue(val_ts.isdisjoint(test_ts))

    def test_6_dataset_split_immutability(self):
        res = split(self.dataset, self.config)
        with self.assertRaises(FrozenInstanceError):
            res.train_dataset = self.dataset

    def test_7_repeated_execution_produces_identical_splits(self):
        res1 = split(self.dataset, self.config)
        res2 = split(self.dataset, self.config)
        self.assertEqual(res1, res2)

    def test_8_original_dataset_remains_unchanged(self):
        orig = tuple(self.dataset.records)
        split(self.dataset, self.config)
        self.assertEqual(self.dataset.records, orig)

    def test_9_boundary_conditions(self):
        empty_ds = Dataset(records=(), feature_names=frozenset(), label_names=frozenset())
        res = split(empty_ds, self.config)
        self.assertEqual(len(res.train_dataset.records), 0)
        self.assertEqual(len(res.validation_dataset.records), 0)
        
        single_ds = Dataset(records=(self.dataset.records[0],), feature_names=frozenset(), label_names=frozenset())
        res2 = split(single_ds, self.config)
        self.assertEqual(len(res2.train_dataset.records), 0)
        self.assertEqual(len(res2.validation_dataset.records), 0)
        self.assertEqual(len(res2.test_dataset.records), 1)

    def test_10_metadata_preservation(self):
        res = split(self.dataset, self.config)
        self.assertEqual(res.train_dataset.metadata, self.dataset.metadata)
        self.assertEqual(res.validation_dataset.metadata, self.dataset.metadata)
        self.assertEqual(res.test_dataset.metadata, self.dataset.metadata)

if __name__ == '__main__':
    unittest.main()
