import os
import glob
import pandas as pd
import json
import traceback

def build_parquets():
    data_dir = r"d:\Gold Scripts\MQL5\Ticks Data\XAUUSD\grid research\apex\data\m1"
    
    # We explicitly only want CSVs directly in data_dir (no subdirectories)
    csv_files = [f for f in glob.glob(os.path.join(data_dir, "*.csv")) if os.path.isfile(f)]
    
    report = {
        "datasets_discovered": len(csv_files),
        "datasets_converted": 0,
        "datasets_skipped": 0,
        "validation_failures": [],
        "performance": []
    }
    
    for csv_file in csv_files:
        filename = os.path.basename(csv_file)
        basename = os.path.splitext(filename)[0]
        parquet_file = os.path.join(data_dir, f"{basename}.parquet")
        csv_size = os.path.getsize(csv_file)
        
        print(f"--- Processing {filename} ---")
        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            report["validation_failures"].append({"file": filename, "error": f"Failed to read CSV: {e}"})
            report["datasets_skipped"] += 1
            continue
            
        # 1. Validation
        try:
            if 'timestamp' not in df.columns:
                raise ValueError("Missing 'timestamp' column")
            
            # Convert timestamp to datetime if it's not already
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            if not df['timestamp'].is_monotonic_increasing:
                raise ValueError("Timestamps are not strictly ascending")
                
            if df['timestamp'].duplicated().any():
                raise ValueError("Duplicate timestamps found")
                
            # OHLC validation
            if df[['open', 'high', 'low', 'close']].isna().any().any():
                raise ValueError("NaN values found in OHLC")
                
            if (df[['open', 'high', 'low', 'close']] < 0).any().any():
                raise ValueError("Negative values found in OHLC")
                
            if (df['high'] < df['low']).any():
                raise ValueError("High < Low found")
                
        except Exception as e:
            print(f"Validation failed for {filename}: {e}")
            report["validation_failures"].append({"file": filename, "error": str(e)})
            report["datasets_skipped"] += 1
            continue
            
        # 2. Conversion
        print(f"Converting {filename} to Parquet...")
        try:
            df.to_parquet(parquet_file, engine='pyarrow', compression='snappy')
        except Exception as e:
            print(f"Conversion failed for {filename}: {e}")
            report["validation_failures"].append({"file": filename, "error": f"Conversion error: {e}"})
            report["datasets_skipped"] += 1
            continue
            
        # 3. Verification
        print(f"Verifying {basename}.parquet...")
        try:
            df_pq = pd.read_parquet(parquet_file, engine='pyarrow')
            
            if len(df) != len(df_pq):
                raise ValueError(f"Row count mismatch: {len(df)} != {len(df_pq)}")
                
            if list(df.columns) != list(df_pq.columns):
                raise ValueError("Column mismatch")
                
            if df['timestamp'].iloc[0] != df_pq['timestamp'].iloc[0]:
                raise ValueError("First timestamp mismatch")
                
            if df['timestamp'].iloc[-1] != df_pq['timestamp'].iloc[-1]:
                raise ValueError("Last timestamp mismatch")
                
        except Exception as e:
            print(f"Verification failed for {basename}.parquet: {e}")
            report["validation_failures"].append({"file": filename, "error": f"Verification error: {e}"})
            report["datasets_skipped"] += 1
            continue
            
        # Calculate performance
        pq_size = os.path.getsize(parquet_file)
        ratio = csv_size / pq_size if pq_size > 0 else 0
        
        report["performance"].append({
            "dataset": basename,
            "csv_size_bytes": csv_size,
            "parquet_size_bytes": pq_size,
            "compression_ratio": ratio,
            "rows": len(df)
        })
        report["datasets_converted"] += 1
        print(f"Success! {basename}: Compressed {csv_size/1024/1024:.1f}MB to {pq_size/1024/1024:.1f}MB ({ratio:.2f}x)")

    # Save report
    report_path = r"C:\Users\User10\.gemini\antigravity-ide\brain\1b73ef8e-c034-4d4f-9ea6-ffe8c7aa8368\parquet_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
        
    print("\n--- Summary ---")
    print(f"Discovered: {report['datasets_discovered']}")
    print(f"Converted:  {report['datasets_converted']}")
    print(f"Skipped:    {report['datasets_skipped']}")

if __name__ == '__main__':
    build_parquets()
