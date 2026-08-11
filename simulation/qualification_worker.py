import pandas as pd
from engine.runtime import ApexRuntime
from engine.logger import EngineLogger
import logging
import time
import os
import sys

def run_simulation(dataset_path: str, log_path: str):
    # Setup logger
    logger_name = 'ApexEngine'
    log = logging.getLogger(logger_name)
    log.handlers.clear() # Clear existing
    
    formatter = logging.Formatter('%(levelname)s | %(message)s') # Strip timestamp for deterministic hashing!
    fh = logging.FileHandler(log_path, mode='w')
    fh.setFormatter(formatter)
    log.addHandler(fh)
    log.setLevel(logging.INFO)
    log.propagate = False
    
    engine_logger = EngineLogger(log_dir=os.path.dirname(log_path))
    engine_logger.logger = log # override
    
    runtime = ApexRuntime(logger=engine_logger)
    
    # Load dataset
    df = pd.read_parquet(dataset_path, engine='pyarrow')
    
    # For speed during multi-run qualification, we use itertuples
    for row in df.itertuples(index=False):
        runtime.on_bar(row.open, row.high, row.low, row.close, row.volume)
        
    return len(df), len(runtime.active_positions)

if __name__ == '__main__':
    dataset = sys.argv[1]
    log_out = sys.argv[2]
    t0 = time.time()
    rows, pos = run_simulation(dataset, log_out)
    t1 = time.time()
    print(f"Processed {rows} rows. Open pos: {pos}. Time: {t1-t0:.2f}s")
