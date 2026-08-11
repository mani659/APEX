import csv
import os
from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Tuple, Dict, Any, Optional

from simulation.market import MarketSnapshot

@dataclass(frozen=True)
class DataLoaderConfig:
    symbol: str
    input_format: str = "csv"
    delimiter: str = ","
    datetime_format: str = "%Y-%m-%d %H:%M:%S"
    timezone: str = "UTC"
    has_header: bool = True
    price_precision: int = 5
    timestamp_column: str = "timestamp"
    bid_column: str = "bid"
    ask_column: str = "ask"
    volume_column: str = "volume"
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

@dataclass(frozen=True)
class DataLoadResult:
    symbol: str
    number_of_records: int
    start_timestamp: int
    end_timestamp: int
    snapshots: Tuple[MarketSnapshot, ...]
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

class DataLoader:
    """
    Strict ingestion layer that loads external market data and converts it into 
    immutable MarketSnapshot objects.
    """
    
    def load_from_csv(self, file_path: str, config: DataLoaderConfig) -> DataLoadResult:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if os.path.getsize(file_path) == 0:
            raise ValueError(f"File is empty: {file_path}")

        snapshots = []
        previous_timestamp = -1
        
        with open(file_path, 'r', encoding='utf-8') as f:
            if config.has_header:
                reader = csv.DictReader(f, delimiter=config.delimiter)
                
                # Verify required columns exist in header
                if reader.fieldnames is None:
                    raise ValueError(f"File has no readable header: {file_path}")
                    
                missing_columns = []
                for col in [config.timestamp_column, config.bid_column, config.ask_column, config.volume_column]:
                    if col not in reader.fieldnames:
                        missing_columns.append(col)
                        
                if missing_columns:
                    raise KeyError(f"Missing required columns in header: {missing_columns}")
                    
                for row_num, row in enumerate(reader, start=2): # header is line 1
                    try:
                        timestamp_str = row[config.timestamp_column]
                        bid_str = row[config.bid_column]
                        ask_str = row[config.ask_column]
                        vol_str = row[config.volume_column]
                        
                        snapshot = self._parse_row(config.symbol, config.datetime_format, timestamp_str, bid_str, ask_str, vol_str)
                        
                        if snapshot.timestamp < previous_timestamp:
                            raise ValueError(f"Chronological ordering violation at row {row_num}: timestamp {snapshot.timestamp} < {previous_timestamp}")
                            
                        snapshots.append(snapshot)
                        previous_timestamp = snapshot.timestamp
                        
                    except Exception as e:
                        raise ValueError(f"Error parsing row {row_num}: {str(e)}") from e
            else:
                reader = csv.reader(f, delimiter=config.delimiter)
                for row_num, row in enumerate(reader, start=1):
                    # For no-header, assume strict order: timestamp, bid, ask, volume
                    if len(row) < 4:
                        raise ValueError(f"Row {row_num} has less than 4 columns (expected timestamp, bid, ask, volume)")
                        
                    try:
                        timestamp_str, bid_str, ask_str, vol_str = row[0], row[1], row[2], row[3]
                        
                        snapshot = self._parse_row(config.symbol, config.datetime_format, timestamp_str, bid_str, ask_str, vol_str)
                        
                        if snapshot.timestamp < previous_timestamp:
                            raise ValueError(f"Chronological ordering violation at row {row_num}: timestamp {snapshot.timestamp} < {previous_timestamp}")
                            
                        snapshots.append(snapshot)
                        previous_timestamp = snapshot.timestamp
                        
                    except Exception as e:
                        raise ValueError(f"Error parsing row {row_num}: {str(e)}") from e

        if not snapshots:
            raise ValueError(f"File contains no valid data rows: {file_path}")
            
        start_ts = snapshots[0].timestamp
        end_ts = snapshots[-1].timestamp
        
        return DataLoadResult(
            symbol=config.symbol,
            number_of_records=len(snapshots),
            start_timestamp=start_ts,
            end_timestamp=end_ts,
            snapshots=tuple(snapshots)
        )
        
    def _parse_row(self, symbol: str, dt_format: str, timestamp_str: str, bid_str: str, ask_str: str, vol_str: str) -> MarketSnapshot:
        # Parse timestamp
        # In a real environment, timezone handling would be here.
        # We assume utc timestamp generation for integer representation.
        try:
            if dt_format == "unix":
                ts = int(float(timestamp_str))
            else:
                dt = datetime.strptime(timestamp_str, dt_format)
                ts = int(dt.replace(tzinfo=None).timestamp())
        except ValueError as e:
            raise ValueError(f"Invalid timestamp format '{timestamp_str}' for format '{dt_format}'") from e
            
        try:
            bid = float(bid_str)
            ask = float(ask_str)
            vol = float(vol_str)
        except ValueError as e:
            raise ValueError(f"Prices and volume must be numeric") from e
            
        if bid <= 0 or ask <= 0:
            raise ValueError("Prices must be strictly positive")
            
        if bid > ask:
            raise ValueError(f"Invalid spread: bid ({bid}) > ask ({ask})")
            
        if vol < 0:
            raise ValueError(f"Volume cannot be negative")
            
        return MarketSnapshot(
            symbol=symbol,
            timestamp=ts,
            bid=bid,
            ask=ask,
            volume=vol
        )
