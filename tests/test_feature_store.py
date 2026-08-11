import unittest
from types import MappingProxyType
from research.pipeline.result import PipelineResult
from research.store.store import FeatureStore
from research.store.errors import DuplicateTimestampError, FeatureNotFoundError
from research.store.query import get_range, first, last

class TestFeatureStore(unittest.TestCase):
    
    def setUp(self):
        self.store = FeatureStore()
        
        self.t1 = PipelineResult(timestamp=100.0, feature_results=MappingProxyType({}))
        self.t2 = PipelineResult(timestamp=200.0, feature_results=MappingProxyType({}))
        self.t3 = PipelineResult(timestamp=300.0, feature_results=MappingProxyType({}))

    def test_add_one_result(self):
        self.store.add(self.t1)
        self.assertEqual(len(self.store), 1)

    def test_retrieve_by_timestamp(self):
        self.store.add(self.t2)
        result = self.store.get(200.0)
        self.assertEqual(result, self.t2)

    def test_retrieve_all_results_chronological(self):
        self.store.add(self.t3)
        self.store.add(self.t1)
        self.store.add(self.t2)
        
        results = self.store.get_all()
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], self.t1)
        self.assertEqual(results[1], self.t2)
        self.assertEqual(results[2], self.t3)

    def test_duplicate_timestamps_raise(self):
        self.store.add(self.t1)
        with self.assertRaises(DuplicateTimestampError):
            self.store.add(self.t1)

    def test_unknown_timestamp_raises(self):
        with self.assertRaises(FeatureNotFoundError):
            self.store.get(999.0)

    def test_returned_collections_are_immutable(self):
        self.store.add(self.t1)
        results = self.store.get_all()
        
        self.assertIsInstance(results, tuple)
        
        # Tuple doesn't support assignment
        with self.assertRaises(TypeError):
            results[0] = self.t2

    def test_store_length_updates(self):
        self.assertEqual(len(self.store), 0)
        self.store.add(self.t1)
        self.assertEqual(len(self.store), 1)
        self.store.add(self.t2)
        self.assertEqual(len(self.store), 2)

    def test_clear_removes_all_entries(self):
        self.store.add(self.t1)
        self.store.add(self.t2)
        self.store.clear()
        self.assertEqual(len(self.store), 0)
        self.assertEqual(len(self.store.get_all()), 0)

    def test_repeated_retrieval_identical(self):
        self.store.add(self.t1)
        result1 = self.store.get(100.0)
        result2 = self.store.get(100.0)
        
        self.assertIs(result1, result2)
        
    def test_query_get_range(self):
        self.store.add(self.t1)
        self.store.add(self.t2)
        self.store.add(self.t3)
        
        range_res = get_range(self.store, 150.0, 350.0)
        self.assertEqual(len(range_res), 2)
        self.assertEqual(range_res[0], self.t2)
        self.assertEqual(range_res[1], self.t3)
        
    def test_query_first_last(self):
        self.store.add(self.t3)
        self.store.add(self.t1)
        self.store.add(self.t2)
        
        self.assertEqual(first(self.store), self.t1)
        self.assertEqual(last(self.store), self.t3)
        
    def test_query_empty_raises(self):
        with self.assertRaises(FeatureNotFoundError):
            first(self.store)
        with self.assertRaises(FeatureNotFoundError):
            last(self.store)

if __name__ == '__main__':
    unittest.main()
