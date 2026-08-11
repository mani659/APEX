import unittest
import statistics
from types import MappingProxyType
from dataclasses import FrozenInstanceError, replace

from research.dataset.result import Dataset, DatasetRecord
from research.analysis.result import FeatureAnalysisResult, FeatureMetrics
from research.analysis.engine import analyze

class TestAnalysisEngine(unittest.TestCase):

    def setUp(self):
        # A dataset with 2 features. 
        # f1: 1.0, 2.0, 3.0, 4.0, 5.0
        # f2: 2.0, None, 4.0, None, 6.0
        records = []
        f1_vals = [1.0, 2.0, 3.0, 4.0, 5.0]
        f2_vals = [2.0, None, 4.0, None, 6.0]
        
        for i in range(5):
            feats = {"f1": f1_vals[i]}
            if f2_vals[i] is not None:
                feats["f2"] = f2_vals[i]
                
            records.append(
                DatasetRecord(
                    timestamp=float(i * 100),
                    features=MappingProxyType(feats),
                    labels=MappingProxyType({"l1": 1.0})
                )
            )
            
        self.dataset = Dataset(
            records=tuple(records),
            feature_names=frozenset({"f1", "f2"}),
            label_names=frozenset({"l1"})
        )
        
        self.f1_vals = f1_vals
        self.f2_vals = [v for v in f2_vals if v is not None]

    def test_1_single_feature_analysis(self):
        single_ds = Dataset(
            records=self.dataset.records,
            feature_names=frozenset({"f1"}),
            label_names=frozenset({"l1"})
        )
        res = analyze(single_ds)
        self.assertEqual(res.feature_count, 1)
        self.assertEqual(res.feature_metrics[0].feature_name, "f1")

    def test_2_multiple_feature_analysis(self):
        res = analyze(self.dataset)
        self.assertEqual(res.feature_count, 2)
        names = [m.feature_name for m in res.feature_metrics]
        self.assertEqual(names, sorted(["f1", "f2"]))

    def test_3_mean_calculation(self):
        res = analyze(self.dataset)
        f1_m = next(m for m in res.feature_metrics if m.feature_name == "f1")
        f2_m = next(m for m in res.feature_metrics if m.feature_name == "f2")
        self.assertEqual(f1_m.mean, statistics.mean(self.f1_vals))
        self.assertEqual(f2_m.mean, statistics.mean(self.f2_vals))

    def test_4_median_calculation(self):
        res = analyze(self.dataset)
        f1_m = next(m for m in res.feature_metrics if m.feature_name == "f1")
        self.assertEqual(f1_m.median, statistics.median(self.f1_vals))

    def test_5_variance_calculation(self):
        res = analyze(self.dataset)
        f1_m = next(m for m in res.feature_metrics if m.feature_name == "f1")
        self.assertEqual(f1_m.variance, statistics.variance(self.f1_vals))

    def test_6_standard_deviation_calculation(self):
        res = analyze(self.dataset)
        f1_m = next(m for m in res.feature_metrics if m.feature_name == "f1")
        self.assertEqual(f1_m.standard_deviation, statistics.stdev(self.f1_vals))

    def test_7_missing_ratio_calculation(self):
        res = analyze(self.dataset)
        f2_m = next(m for m in res.feature_metrics if m.feature_name == "f2")
        self.assertEqual(f2_m.missing_ratio, 0.4) # 2 out of 5

    def test_8_feature_analysis_result_immutability(self):
        res = analyze(self.dataset)
        with self.assertRaises(FrozenInstanceError):
            res.feature_count = 10

    def test_9_repeated_execution_produces_identical_output(self):
        res1 = analyze(self.dataset)
        res2 = analyze(self.dataset)
        r1 = replace(res1, analyzed_timestamp="")
        r2 = replace(res2, analyzed_timestamp="")
        self.assertEqual(r1, r2)

    def test_10_dataset_unchanged_after_analysis(self):
        orig = tuple(self.dataset.records)
        res = analyze(self.dataset)
        self.assertEqual(self.dataset.records, orig)

if __name__ == '__main__':
    unittest.main()
