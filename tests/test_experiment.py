import unittest
from types import MappingProxyType
from dataclasses import FrozenInstanceError, replace
from unittest.mock import MagicMock

from research.dataset.result import Dataset, DatasetRecord
from research.splitting.config import SplitConfig
from research.splitting.result import DatasetSplit
from research.validation.report import ValidationReport, ValidationIssue, Severity
from research.analysis.result import FeatureAnalysisResult, FeatureMetrics

from research.experiment.config import ExperimentConfig
from research.experiment.result import ExperimentRecord
from research.experiment.engine import run
from research.experiment.errors import ExperimentExecutionError

class TestExperimentEngine(unittest.TestCase):
    
    def setUp(self):
        records = []
        for i in range(10):
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
        
        self.split_config = SplitConfig(train_ratio=0.6, validation_ratio=0.2, test_ratio=0.2)
        self.config = ExperimentConfig(
            experiment_name="Exp_V1",
            experiment_version="1.0.0",
            split_config=self.split_config,
            metadata=MappingProxyType({"author": "Apex"})
        )

    def test_1_successful_experiment_orchestration(self):
        record = run(self.dataset, self.config)
        self.assertEqual(record.experiment_name, "Exp_V1")
        self.assertTrue(record.validation_report.valid)
        self.assertEqual(record.feature_analysis.feature_count, 1)
        self.assertEqual(len(record.dataset_split.train_dataset.records), 6)

    def test_2_validation_failure_stops_execution(self):
        def mock_validator(ds):
            return ValidationReport(
                valid=False,
                issue_count=1,
                error_count=1,
                warning_count=0,
                issues=(ValidationIssue(Severity.ERROR, "Cat", "Msg"),)
            )
            
        with self.assertRaises(ExperimentExecutionError):
            run(self.dataset, self.config, validator_fn=mock_validator)

    def test_3_execution_order(self):
        order = []
        
        def mock_val(ds):
            order.append("validation")
            return ValidationReport(True, 0, 0, 0, ())
            
        def mock_ana(ds):
            order.append("analysis")
            return FeatureAnalysisResult(1, "", ())
            
        def mock_spl(ds, cfg):
            order.append("splitting")
            return DatasetSplit(ds, ds, ds, cfg)
            
        run(
            self.dataset, self.config,
            validator_fn=mock_val,
            analyzer_fn=mock_ana,
            splitter_fn=mock_spl
        )
        
        self.assertEqual(order, ["validation", "analysis", "splitting"])

    def test_4_experiment_record_immutability(self):
        record = run(self.dataset, self.config)
        with self.assertRaises(FrozenInstanceError):
            record.experiment_name = "Hacked"

    def test_5_repeated_execution_produces_identical_records(self):
        r1 = run(self.dataset, self.config)
        r2 = run(self.dataset, self.config)
        
        r1 = replace(r1, created_timestamp="")
        ana1 = replace(r1.feature_analysis, analyzed_timestamp="")
        r1 = replace(r1, feature_analysis=ana1)
        
        r2 = replace(r2, created_timestamp="")
        ana2 = replace(r2.feature_analysis, analyzed_timestamp="")
        r2 = replace(r2, feature_analysis=ana2)
        
        self.assertEqual(r1, r2)

    def test_6_original_dataset_remains_unchanged(self):
        orig = tuple(self.dataset.records)
        run(self.dataset, self.config)
        self.assertEqual(self.dataset.records, orig)

    def test_7_configuration_immutability(self):
        with self.assertRaises(FrozenInstanceError):
            self.config.experiment_name = "Hack"

    def test_8_metadata_preservation(self):
        record = run(self.dataset, self.config)
        self.assertEqual(record.metadata, self.config.metadata)

    def test_9_dependency_injection_using_mock_engines(self):
        mock_val = MagicMock(return_value=ValidationReport(True, 0, 0, 0, ()))
        mock_ana = MagicMock(return_value=FeatureAnalysisResult(1, "", ()))
        mock_spl = MagicMock(return_value=DatasetSplit(self.dataset, self.dataset, self.dataset, self.split_config))
        
        run(
            self.dataset, self.config,
            validator_fn=mock_val,
            analyzer_fn=mock_ana,
            splitter_fn=mock_spl
        )
        
        mock_val.assert_called_once_with(self.dataset)
        mock_ana.assert_called_once_with(self.dataset)
        mock_spl.assert_called_once_with(self.dataset, self.config.split_config)

    def test_10_no_hidden_state_between_repeated_experiments(self):
        r1 = run(self.dataset, self.config)
        r2 = run(self.dataset, self.config)
        r3 = run(self.dataset, self.config)
        self.assertEqual(len(r1.dataset_split.train_dataset.records), 6)
        self.assertEqual(len(r2.dataset_split.train_dataset.records), 6)
        self.assertEqual(len(r3.dataset_split.train_dataset.records), 6)

if __name__ == '__main__':
    unittest.main()
