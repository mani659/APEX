import unittest
import json
from dataclasses import FrozenInstanceError, dataclass
from datetime import datetime
from types import MappingProxyType

from simulation.data_exporter import DataExporter, DataExporterConfig, ExportResult
from simulation.market import MarketSnapshot

@dataclass(frozen=True)
class MockStats:
    net_profit: float
    trades: int
    metadata: MappingProxyType

class TestDataExporter(unittest.TestCase):
    
    def setUp(self):
        self.exporter = DataExporter()
        
        self.snapshots = [
            MarketSnapshot(symbol="EURUSD", timestamp=1672567200, bid=1.0500, ask=1.0501, volume=100.0),
            MarketSnapshot(symbol="EURUSD", timestamp=1672567260, bid=1.0502, ask=1.0503, volume=150.0)
        ]
        
        self.stats = MockStats(
            net_profit=100.50,
            trades=5,
            metadata=MappingProxyType({"author": "test"})
        )

    def test_csv_export_list_with_headers(self):
        config = DataExporterConfig(output_format="csv", include_headers=True)
        result = self.exporter.export(self.snapshots, config)
        
        self.assertEqual(result.number_of_records, 2)
        self.assertEqual(result.format, "csv")
        
        lines = result.serialized_output.strip().split('\n')
        self.assertEqual(len(lines), 3) # Header + 2 rows
        self.assertEqual(lines[0], "symbol,timestamp,bid,ask,volume")
        self.assertTrue("EURUSD,1672567200,1.05,1.0501,100.0" in lines[1])

    def test_csv_export_list_without_headers(self):
        config = DataExporterConfig(output_format="csv", include_headers=False)
        result = self.exporter.export(self.snapshots, config)
        
        lines = result.serialized_output.strip().split('\n')
        self.assertEqual(len(lines), 2)
        self.assertTrue("EURUSD,1672567200,1.05,1.0501,100.0" in lines[0])

    def test_json_export_list_pretty_print(self):
        config = DataExporterConfig(output_format="json", pretty_print=True)
        result = self.exporter.export(self.snapshots, config)
        
        self.assertEqual(result.number_of_records, 2)
        
        parsed = json.loads(result.serialized_output)
        self.assertIsInstance(parsed, list)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["symbol"], "EURUSD")
        self.assertEqual(parsed[0]["timestamp"], 1672567200)
        
        # Pretty print has multiple lines
        self.assertGreater(len(result.serialized_output.split('\n')), 2)

    def test_json_export_single_object(self):
        config = DataExporterConfig(output_format="json", pretty_print=False)
        result = self.exporter.export(self.stats, config)
        
        self.assertEqual(result.number_of_records, 1)
        
        parsed = json.loads(result.serialized_output)
        self.assertIsInstance(parsed, dict)
        self.assertEqual(parsed["net_profit"], 100.5)
        self.assertEqual(parsed["metadata"]["author"], "test")

    def test_empty_collections(self):
        config_csv = DataExporterConfig(output_format="csv")
        result_csv = self.exporter.export([], config_csv)
        self.assertEqual(result_csv.serialized_output, "")
        self.assertEqual(result_csv.number_of_records, 0)
        
        config_json = DataExporterConfig(output_format="json")
        result_json = self.exporter.export([], config_json)
        self.assertEqual(result_json.serialized_output, "[]")
        self.assertEqual(result_json.number_of_records, 0)

    def test_export_immutability(self):
        config = DataExporterConfig(output_format="json")
        result = self.exporter.export(self.snapshots, config)
        
        with self.assertRaises(FrozenInstanceError):
            result.number_of_records = 5

    def test_deterministic_json_output(self):
        config = DataExporterConfig(output_format="json", pretty_print=False)
        
        result1 = self.exporter.export(self.stats, config)
        result2 = self.exporter.export(self.stats, config)
        
        self.assertEqual(result1.serialized_output, result2.serialized_output)
        
    def test_invalid_format(self):
        config = DataExporterConfig(output_format="xml")
        with self.assertRaises(ValueError):
            self.exporter.export(self.snapshots, config)

if __name__ == '__main__':
    unittest.main()
