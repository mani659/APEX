import unittest
from types import MappingProxyType
from dataclasses import FrozenInstanceError

from research.dataset.result import Dataset, DatasetRecord
from research.validation.report import ValidationReport, ValidationIssue, Severity
from research.validation.engine import validate
from research.validation.errors import DatasetValidationError

class TestValidationEngine(unittest.TestCase):
    
    def setUp(self):
        self.valid_record_1 = DatasetRecord(
            timestamp=100.0,
            features=MappingProxyType({"f1": 1.0, "f2": 2.0}),
            labels=MappingProxyType({"l1": 0.0})
        )
        self.valid_record_2 = DatasetRecord(
            timestamp=200.0,
            features=MappingProxyType({"f1": 3.0, "f2": 4.0}),
            labels=MappingProxyType({"l1": 1.0})
        )
        
        self.valid_dataset = Dataset(
            records=(self.valid_record_1, self.valid_record_2),
            feature_names=frozenset({"f1", "f2"}),
            label_names=frozenset({"l1"}),
            metadata=MappingProxyType({"version": "1.0"})
        )

    def test_1_valid_dataset_returns_clean_report(self):
        report = validate(self.valid_dataset)
        self.assertTrue(report.valid)
        self.assertEqual(report.issue_count, 0)
        self.assertEqual(report.error_count, 0)

    def test_2_empty_dataset_produces_error(self):
        empty_dataset = Dataset(
            records=(),
            feature_names=frozenset({"f1"}),
            label_names=frozenset({"l1"}),
            metadata=MappingProxyType({})
        )
        report = validate(empty_dataset)
        self.assertFalse(report.valid)
        self.assertEqual(report.error_count, 1)
        self.assertEqual(report.issues[0].category, "Dataset Size")

    def test_3_duplicate_timestamps_produces_error(self):
        dup_record = DatasetRecord(
            timestamp=100.0, # Duplicate!
            features=MappingProxyType({"f1": 5.0, "f2": 6.0}),
            labels=MappingProxyType({"l1": 1.0})
        )
        ds = Dataset(
            records=(self.valid_record_1, dup_record),
            feature_names=frozenset({"f1", "f2"}),
            label_names=frozenset({"l1"}),
            metadata=MappingProxyType({})
        )
        report = validate(ds)
        self.assertFalse(report.valid)
        self.assertTrue(any(iss.category == "Duplicate Timestamp" for iss in report.issues))

    def test_4_missing_feature_produces_error(self):
        bad_record = DatasetRecord(
            timestamp=200.0,
            features=MappingProxyType({"f1": 3.0}), # Missing f2
            labels=MappingProxyType({"l1": 1.0})
        )
        ds = Dataset(
            records=(self.valid_record_1, bad_record),
            feature_names=frozenset({"f1", "f2"}),
            label_names=frozenset({"l1"}),
            metadata=MappingProxyType({})
        )
        report = validate(ds)
        self.assertFalse(report.valid)
        self.assertTrue(any(iss.category == "Missing Feature" for iss in report.issues))
        
    def test_5_missing_label_produces_error(self):
        bad_record = DatasetRecord(
            timestamp=200.0,
            features=MappingProxyType({"f1": 3.0, "f2": 4.0}),
            labels=MappingProxyType({}) # Missing l1
        )
        ds = Dataset(
            records=(self.valid_record_1, bad_record),
            feature_names=frozenset({"f1", "f2"}),
            label_names=frozenset({"l1"}),
            metadata=MappingProxyType({})
        )
        report = validate(ds)
        self.assertFalse(report.valid)
        self.assertTrue(any(iss.category == "Missing Label" for iss in report.issues))

    def test_6_out_of_order_timestamps_produces_error(self):
        ds = Dataset(
            records=(self.valid_record_2, self.valid_record_1), # 200 then 100
            feature_names=frozenset({"f1", "f2"}),
            label_names=frozenset({"l1"}),
            metadata=MappingProxyType({})
        )
        report = validate(ds)
        self.assertFalse(report.valid)
        self.assertTrue(any(iss.category == "Timestamp Ordering" for iss in report.issues))

    def test_7_validation_report_immutability(self):
        report = validate(self.valid_dataset)
        with self.assertRaises(FrozenInstanceError):
            report.valid = False

    def test_8_validation_issue_immutability(self):
        issue = ValidationIssue(severity=Severity.ERROR, category="Test", message="Test")
        with self.assertRaises(FrozenInstanceError):
            issue.message = "Changed"

    def test_9_repeated_execution_produces_identical_report(self):
        report1 = validate(self.valid_dataset)
        report2 = validate(self.valid_dataset)
        self.assertEqual(report1, report2)

    def test_10_dataset_unchanged_after_validation(self):
        original_records = tuple(self.valid_dataset.records)
        report = validate(self.valid_dataset)
        self.assertEqual(self.valid_dataset.records, original_records)

if __name__ == '__main__':
    unittest.main()
