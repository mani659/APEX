import json
import os
import time
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class TelemetryEvent:
    trace_id: str
    historical_timestamp: str
    symbol: str
    module: str
    layer: str
    event_type: str
    decision_state: str
    tick_number: int
    context: Dict[str, Any]

class TelemetryLayer:
    def __init__(self, log_dir: str = "telemetry_logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.file_handles = {}
        self.tick_counter = 0

    def emit(self, trace_id: str, ts: str, symbol: str, module: str, layer: str, 
             event_type: str, decision_state: str, context: Dict[str, Any]):
        self.tick_counter += 1
        event = TelemetryEvent(
            trace_id=trace_id,
            historical_timestamp=str(ts),
            symbol=symbol,
            module=module,
            layer=layer,
            event_type=event_type,
            decision_state=decision_state,
            tick_number=self.tick_counter,
            context=context
        )
        
        file_path = os.path.join(self.log_dir, f"{symbol}_telemetry.jsonl")
        
        if symbol not in self.file_handles:
            self.file_handles[symbol] = open(file_path, "a")
            
        self.file_handles[symbol].write(json.dumps(asdict(event)) + "\n")

    def close(self):
        for fh in self.file_handles.values():
            fh.close()
        self.file_handles.clear()

def compile_to_parquet(jsonl_path: str, output_path: str):
    import pandas as pd
    if not os.path.exists(jsonl_path):
        return
    df = pd.read_json(jsonl_path, lines=True)
    # Context is a dict, we can keep it as an object column or flatten it
    df.to_parquet(output_path, index=False)
