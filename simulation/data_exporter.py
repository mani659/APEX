import csv
import io
import json
import enum
from dataclasses import dataclass, field, is_dataclass, asdict
from datetime import datetime
from types import MappingProxyType
from typing import Any, List, Dict, Union, Iterable

@dataclass(frozen=True)
class DataExporterConfig:
    output_format: str = "json"  # "csv" or "json"
    delimiter: str = ","
    datetime_format: str = "%Y-%m-%d %H:%M:%S"
    include_headers: bool = True
    pretty_print: bool = True
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

@dataclass(frozen=True)
class ExportResult:
    format: str
    number_of_records: int
    serialized_output: str
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

class ImmutableJSONEncoder(json.JSONEncoder):
    def __init__(self, dt_format: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dt_format = dt_format

    def default(self, obj: Any) -> Any:
        from dataclasses import fields
        if is_dataclass(obj):
            return {f.name: getattr(obj, f.name) for f in fields(obj)}
        if isinstance(obj, enum.Enum):
            return obj.name
        if isinstance(obj, datetime):
            if self.dt_format == "unix":
                return int(obj.timestamp())
            return obj.strftime(self.dt_format)
        if isinstance(obj, MappingProxyType):
            return dict(obj)
        # Fallback
        return super().default(obj)

class DataExporter:
    """
    Serializes immutable framework DTOs into deterministic strings (CSV or JSON).
    Performs no calculation, no file writing, and does not repair data.
    """
    
    def export(self, data: Any, config: DataExporterConfig) -> ExportResult:
        if config.output_format.lower() not in ["csv", "json"]:
            raise ValueError(f"Unsupported export format: {config.output_format}")

        if config.output_format.lower() == "csv":
            return self._export_csv(data, config)
        else:
            return self._export_json(data, config)

    def _export_csv(self, data: Any, config: DataExporterConfig) -> ExportResult:
        # Normalize input to an iterable
        if not isinstance(data, (list, tuple)):
            data_list = [data]
        else:
            data_list = data
            
        if not data_list:
            return ExportResult(
                format="csv",
                number_of_records=0,
                serialized_output=""
            )
            
        # Verify elements are dataclasses
        first_item = data_list[0]
        if not is_dataclass(first_item):
            raise ValueError("CSV export requires a list of dataclasses (e.g. MarketSnapshot, Trade)")
            
        # Try to flatten slightly, but mostly for simple tabular data
        # If there are nested lists/dicts, they will just stringify which is acceptable for raw CSV
        
        output = io.StringIO()
        writer = csv.writer(output, delimiter=config.delimiter, lineterminator='\n')
        
        from dataclasses import fields
        # Extract headers
        dict_rep = {f.name: getattr(first_item, f.name) for f in fields(first_item)}
        headers = list(dict_rep.keys())
        
        if config.include_headers:
            writer.writerow(headers)
            
        for item in data_list:
            if not is_dataclass(item):
                raise ValueError("Mixed types in collection for CSV export is not supported")
            
            row_dict = {f.name: getattr(item, f.name) for f in fields(item)}
            row_values = []
            for h in headers:
                val = row_dict.get(h)
                if isinstance(val, enum.Enum):
                    row_values.append(val.name)
                elif isinstance(val, datetime):
                    if config.datetime_format == "unix":
                        row_values.append(str(int(val.timestamp())))
                    else:
                        row_values.append(val.strftime(config.datetime_format))
                elif isinstance(val, MappingProxyType):
                    # For CSV, complex types stringify
                    row_values.append(json.dumps(dict(val)))
                elif isinstance(val, (dict, list, tuple)):
                    row_values.append(json.dumps(val))
                else:
                    row_values.append(str(val) if val is not None else "")
            writer.writerow(row_values)
            
        return ExportResult(
            format="csv",
            number_of_records=len(data_list),
            serialized_output=output.getvalue()
        )

    def _export_json(self, data: Any, config: DataExporterConfig) -> ExportResult:
        if not isinstance(data, (list, tuple)):
            data_list = [data]
            is_single = True
        else:
            data_list = data
            is_single = False
            
        if not data_list:
            return ExportResult(
                format="json",
                number_of_records=0,
                serialized_output="[]"
            )

        indent = 4 if config.pretty_print else None
        
        encoder = ImmutableJSONEncoder(
            dt_format=config.datetime_format,
            indent=indent,
            sort_keys=True # Ensure determinism in dictionary keys
        )
        
        target = data if not is_single else data_list[0]
        
        serialized = encoder.encode(target)
        
        return ExportResult(
            format="json",
            number_of_records=len(data_list),
            serialized_output=serialized
        )
