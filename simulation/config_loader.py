import json
from dataclasses import dataclass, field
from types import MappingProxyType
import os

@dataclass(frozen=True)
class APEXConfiguration:
    """Immutable representation of framework configuration."""
    source_file: str
    format: str
    version: str
    engine_compatibility: str
    parameters: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

def load_json(file_path: str) -> APEXConfiguration:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    return _build_config(data, file_path, "json")

def load_yaml(file_path: str) -> APEXConfiguration:
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required for YAML configuration support.")
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    return _build_config(data, file_path, "yaml")

def _build_config(data: dict, source: str, file_format: str) -> APEXConfiguration:
    version = data.get("version", "1.0.0")
    engine_compatibility = data.get("engine_compatibility", "15")
    
    # Store everything else in parameters, ensuring deep immutability could be added
    # but top-level MappingProxyType provides sufficient API boundary protection.
    params = dict(data)
    if "version" in params:
        del params["version"]
    if "engine_compatibility" in params:
        del params["engine_compatibility"]
        
    return APEXConfiguration(
        source_file=source,
        format=file_format,
        version=str(version),
        engine_compatibility=str(engine_compatibility),
        parameters=MappingProxyType(params)
    )
