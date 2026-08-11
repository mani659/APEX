import unittest
import os
import tempfile
from dataclasses import FrozenInstanceError

from simulation.data_loader import DataLoader, DataLoaderConfig, DataLoadResult
from simulation.market import MarketSnapshot

class TestDataLoader(unittest.TestCase):
    
    def setUp(self):
        self.loader = DataLoader()
        self.config = DataLoaderConfig(
            symbol="EURUSD",
            datetime_format="%Y-%m-%d %H:%M:%S"
        )
        
    def _create_temp_csv(self, content: str) -> str:
        fd, path = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    def test_valid_csv_loading(self):
        csv_content = (
            "timestamp,bid,ask,volume\n"
            "2023-01-01 10:00:00,1.0500,1.0501,100\n"
            "2023-01-01 10:01:00,1.0502,1.0503,150\n"
        )
        path = self._create_temp_csv(csv_content)
        try:
            result = self.loader.load_from_csv(path, self.config)
            
            self.assertEqual(result.number_of_records, 2)
            self.assertEqual(result.symbol, "EURUSD")
            self.assertEqual(len(result.snapshots), 2)
            
            s1 = result.snapshots[0]
            self.assertEqual(s1.bid, 1.0500)
            self.assertEqual(s1.ask, 1.0501)
            self.assertEqual(s1.volume, 100.0)
            
            s2 = result.snapshots[1]
            self.assertGreater(s2.timestamp, s1.timestamp)
            
            # Test strict output immutability (tuple of MarketSnapshot)
            self.assertIsInstance(result.snapshots, tuple)
            with self.assertRaises(FrozenInstanceError):
                result.snapshots[0].bid = 2.0
                
        finally:
            os.remove(path)

    def test_missing_columns(self):
        csv_content = (
            "timestamp,bid,volume\n" # Missing 'ask'
            "2023-01-01 10:00:00,1.0500,100\n"
        )
        path = self._create_temp_csv(csv_content)
        try:
            with self.assertRaises(KeyError) as ctx:
                self.loader.load_from_csv(path, self.config)
            self.assertIn("Missing required columns in header", str(ctx.exception))
        finally:
            os.remove(path)

    def test_invalid_timestamps(self):
        csv_content = (
            "timestamp,bid,ask,volume\n"
            "INVALID_TIME,1.0500,1.0501,100\n"
        )
        path = self._create_temp_csv(csv_content)
        try:
            with self.assertRaises(ValueError) as ctx:
                self.loader.load_from_csv(path, self.config)
            self.assertIn("Invalid timestamp format", str(ctx.exception))
        finally:
            os.remove(path)

    def test_invalid_prices(self):
        csv_content = (
            "timestamp,bid,ask,volume\n"
            "2023-01-01 10:00:00,abc,1.0501,100\n"
        )
        path = self._create_temp_csv(csv_content)
        try:
            with self.assertRaises(ValueError) as ctx:
                self.loader.load_from_csv(path, self.config)
            self.assertIn("Prices and volume must be numeric", str(ctx.exception))
        finally:
            os.remove(path)

    def test_bid_greater_than_ask_failure(self):
        csv_content = (
            "timestamp,bid,ask,volume\n"
            "2023-01-01 10:00:00,1.0502,1.0501,100\n"
        )
        path = self._create_temp_csv(csv_content)
        try:
            with self.assertRaises(ValueError) as ctx:
                self.loader.load_from_csv(path, self.config)
            self.assertIn("Invalid spread", str(ctx.exception))
        finally:
            os.remove(path)

    def test_chronological_ordering_failure(self):
        csv_content = (
            "timestamp,bid,ask,volume\n"
            "2023-01-01 10:02:00,1.0500,1.0501,100\n"
            "2023-01-01 10:01:00,1.0502,1.0503,150\n"
        )
        path = self._create_temp_csv(csv_content)
        try:
            with self.assertRaises(ValueError) as ctx:
                self.loader.load_from_csv(path, self.config)
            self.assertIn("Chronological ordering violation", str(ctx.exception))
        finally:
            os.remove(path)

    def test_empty_file_behavior(self):
        path = self._create_temp_csv("")
        try:
            with self.assertRaises(ValueError) as ctx:
                self.loader.load_from_csv(path, self.config)
            self.assertIn("File is empty", str(ctx.exception))
        finally:
            os.remove(path)
            
    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.loader.load_from_csv("does_not_exist.csv", self.config)

    def test_single_row_execution(self):
        csv_content = (
            "timestamp,bid,ask,volume\n"
            "2023-01-01 10:00:00,1.0500,1.0501,100\n"
        )
        path = self._create_temp_csv(csv_content)
        try:
            result = self.loader.load_from_csv(path, self.config)
            self.assertEqual(result.number_of_records, 1)
            self.assertEqual(result.start_timestamp, result.end_timestamp)
        finally:
            os.remove(path)
            
    def test_unix_timestamp_parsing(self):
        config_unix = DataLoaderConfig(
            symbol="EURUSD",
            datetime_format="unix"
        )
        csv_content = (
            "timestamp,bid,ask,volume\n"
            "1672567200,1.0500,1.0501,100\n"
        )
        path = self._create_temp_csv(csv_content)
        try:
            result = self.loader.load_from_csv(path, config_unix)
            self.assertEqual(result.snapshots[0].timestamp, 1672567200)
        finally:
            os.remove(path)

if __name__ == '__main__':
    unittest.main()
