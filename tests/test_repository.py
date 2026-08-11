import unittest
import os
import shutil
import unittest.mock
from types import MappingProxyType
from dataclasses import FrozenInstanceError

from research.dataset.result import Dataset, DatasetRecord
from research.splitting.config import SplitConfig
from research.splitting.result import DatasetSplit
from research.validation.report import ValidationReport, ValidationIssue, Severity
from research.analysis.result import FeatureAnalysisResult, FeatureMetrics

from research.experiment.config import ExperimentConfig
from research.experiment.result import ExperimentRecord

from research.repository.config import RepositoryConfig
from research.repository.result import RepositoryEntry
from research.repository.errors import DuplicateExperimentError, RepositoryReadError
from research.repository.engine import ExperimentRepository

class TestExperimentRepository(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = "test_repo_dir"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
        self.config = RepositoryConfig(repository_path=self.test_dir, overwrite_existing=False)
        self.repo = ExperimentRepository(self.config)
        
        records = tuple(
            DatasetRecord(
                timestamp=float(i), 
                features=MappingProxyType({"f1": float(i)}), 
                labels=MappingProxyType({"l1": 1.0})
            )
            for i in range(2)
        )
        ds = Dataset(records, frozenset({"f1"}), frozenset({"l1"}))
        
        val = ValidationReport(True, 0, 0, 0, tuple())
        ana = FeatureAnalysisResult(1, "2026-01-01T00:00:00", tuple())
        spl = DatasetSplit(ds, ds, ds, SplitConfig(0.5, 0.25, 0.25))
        
        self.record = ExperimentRecord(
            experiment_name="RepoTest",
            experiment_version="1.0",
            created_timestamp="2026-01-01T00:00:00",
            validation_report=val,
            feature_analysis=ana,
            dataset_split=spl
        )

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_1_save_experiment(self):
        entry = self.repo.save(self.record)
        self.assertEqual(entry.experiment_id, "experiment_000001")
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "experiment_000001.json")))

    def test_2_load_experiment(self):
        entry1 = self.repo.save(self.record)
        entry2 = self.repo.load(entry1.experiment_id)
        self.assertEqual(entry1.experiment_id, entry2.experiment_id)
        self.assertEqual(entry1.created_timestamp, entry2.created_timestamp)
        self.assertEqual(entry2.experiment_record.experiment_name, "RepoTest")

    def test_3_duplicate_experiment_rejected(self):
        entry = self.repo.save(self.record)
        
        with unittest.mock.patch.object(self.repo, 'list', return_value=[]):
            with self.assertRaises(DuplicateExperimentError):
                self.repo.save(self.record)

    def test_4_repository_listing(self):
        self.repo.save(self.record)
        self.repo.save(self.record)
        lst = self.repo.list()
        self.assertEqual(len(lst), 2)
        self.assertIn("experiment_000001", lst)
        self.assertIn("experiment_000002", lst)

    def test_5_exists_correctness(self):
        self.assertFalse(self.repo.exists("experiment_000001"))
        self.repo.save(self.record)
        self.assertTrue(self.repo.exists("experiment_000001"))

    def test_6_round_trip_serialization(self):
        entry1 = self.repo.save(self.record)
        entry2 = self.repo.load(entry1.experiment_id)
        self.assertEqual(entry1, entry2)

    def test_7_repository_entry_immutability(self):
        entry = self.repo.save(self.record)
        with self.assertRaises(FrozenInstanceError):
            entry.experiment_id = "test"

    def test_8_repeated_loads_produce_identical_objects(self):
        entry1 = self.repo.save(self.record)
        l1 = self.repo.load(entry1.experiment_id)
        l2 = self.repo.load(entry1.experiment_id)
        self.assertEqual(l1, l2)

    def test_9_repository_never_mutates_experiment_record(self):
        orig_name = self.record.experiment_name
        self.repo.save(self.record)
        self.assertEqual(self.record.experiment_name, orig_name)

    def test_10_filesystem_layout_deterministic(self):
        self.repo.save(self.record)
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, "experiment_000001.json")))

if __name__ == '__main__':
    unittest.main()
