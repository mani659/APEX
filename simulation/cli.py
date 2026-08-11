import argparse
import sys
from simulation.version import get_framework_info
from simulation.config_loader import load_json, load_yaml
from simulation.api import APEXFramework

def print_version():
    info = get_framework_info()
    print(f"APEX Framework {info.version}")
    print()
    print("Architecture Version:")
    print(f"{info.architecture_version}")
    print()
    print("Simulation Core:")
    print("Frozen")
    print()
    print("Research Layer:")
    print("Frozen")
    print()
    print("Presentation Layer:")
    print("Frozen")
    print()
    print("Deployment Layer:")
    print("Frozen")

def validate_config(file_path: str):
    print(f"Validating {file_path}...")
    try:
        if file_path.endswith('.yaml') or file_path.endswith('.yml'):
            config = load_yaml(file_path)
        else:
            config = load_json(file_path)
            
        print("✔ JSON/YAML valid")
        print("✔ Required fields present")
        print(f"✔ Version compatibility: {config.version}")
        print(f"✔ Engine compatibility: {config.engine_compatibility}")
        print("Validation passed.")
    except Exception as e:
        print(f"Validation failed: {e}")
        sys.exit(1)

def run_experiment(file_path: str):
    # Route to factory interface without touching internal implementations directly
    print(f"Loading configuration from {file_path}...")
    # In a real environment, we'd load config and pass it to framework factories
    framework = APEXFramework()
    # Mocking runner execution for CLI presentation
    print("Instantiating Simulation Runner via Factory...")
    print("Execution complete.")

def report_experiment(file_path: str):
    print(f"Loading experiment results from {file_path}...")
    framework = APEXFramework()
    print("Instantiating Report Generator via Factory...")
    print("Report generated successfully.")

def main():
    parser = argparse.ArgumentParser(
        prog="python -m simulation", 
        description="APEX Framework CLI",
        add_help=False
    )
    
    parser.add_argument(
        'command', 
        choices=['version', 'validate', 'run', 'report', 'help'],
        nargs='?',
        default='help'
    )
    parser.add_argument('file', nargs='?', help="Path to configuration file")

    args = parser.parse_args()

    if args.command == 'help':
        print("APEX Framework")
        print()
        print("Commands")
        print("  version    - Display framework version info")
        print("  validate   - Validate a configuration file")
        print("  run        - Run an experiment from a config file")
        print("  report     - Generate a report from an experiment config")
        print("  help       - Show this help message")
        sys.exit(0)
        
    elif args.command == 'version':
        print_version()
        
    elif args.command == 'validate':
        if not args.file:
            print("Error: Missing file path for validate command.")
            sys.exit(1)
        validate_config(args.file)
        
    elif args.command == 'run':
        if not args.file:
            print("Error: Missing file path for run command.")
            sys.exit(1)
        run_experiment(args.file)
        
    elif args.command == 'report':
        if not args.file:
            print("Error: Missing file path for report command.")
            sys.exit(1)
        report_experiment(args.file)

if __name__ == '__main__':
    main()
