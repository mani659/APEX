import unittest
import json
import os
import sys
from io import StringIO
from unittest.mock import patch
from simulation.cli import main
from simulation.config_loader import load_json, load_yaml, APEXConfiguration

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.test_json_path = "test_config.json"
        with open(self.test_json_path, "w") as f:
            json.dump({
                "version": "1.0.0",
                "engine_compatibility": "15",
                "some_param": "value"
            }, f)
            
    def tearDown(self):
        if os.path.exists(self.test_json_path):
            os.remove(self.test_json_path)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['apex', 'version'])
    def test_version_command(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("APEX Framework", output)
        self.assertIn("Architecture Version:", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['apex', 'help'])
    def test_help_command(self, mock_stdout):
        try:
            main()
        except SystemExit:
            pass
        output = mock_stdout.getvalue()
        self.assertIn("Commands", output)
        self.assertIn("version", output)
        self.assertIn("validate", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['apex', 'validate', 'test_config.json'])
    def test_validate_command(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("✔ JSON/YAML valid", output)

    def test_config_loader_json(self):
        config = load_json(self.test_json_path)
        self.assertIsInstance(config, APEXConfiguration)
        self.assertEqual(config.version, "1.0.0")
        self.assertEqual(config.parameters["some_param"], "value")

    def test_yaml_fallback(self):
        try:
            import yaml
            has_yaml = True
        except ImportError:
            has_yaml = False
            
        if not has_yaml:
            with self.assertRaises(ImportError):
                load_yaml("test_config.yaml")

if __name__ == '__main__':
    unittest.main()
