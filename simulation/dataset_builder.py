import os
import glob
import pandas as pd
import json

def build_dataset():
    data_dir = r"d:\Gold Scripts\MQL5\Ticks Data\XAUUSD\grid research\apex\data\m1\EUR"
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    all_dfs = []
    
    report = {
        "files_processed": len(csv_files),
        "total_raw_rows": 0,
        "anomalies": {
            "high_less_than_low": 0,
            "negative_prices": 0,
            "nan_values": 0,
            "zero_prices": 0
        },
        "duplicates_removed": 0,
        "corrupted_rows_removed": 0
    }
    
    print(f"Discovered {len(csv_files)} files. Processing...")
    
    for f in csv_files:
        try:
            df = pd.read_csv(f, header=None, names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
            report["total_raw_rows"] += len(df)
            
            # Create timestamp
            # MT5 format: YYYY.MM.DD HH:MM
            df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y.%m.%d %H:%M')
            df.drop(columns=['date', 'time'], inplace=True)
            
            all_dfs.append(df)
        except Exception as e:
            print(f"Error reading {f}: {e}")
            
    if not all_dfs:
        print("No data found!")
        return
        
    master_df = pd.concat(all_dfs, ignore_index=True)
    
    # Validation / Detection
    nan_mask = master_df.isna().any(axis=1)
    neg_mask = (master_df['open'] < 0) | (master_df['high'] < 0) | (master_df['low'] < 0) | (master_df['close'] < 0)
    zero_mask = (master_df['open'] == 0) | (master_df['high'] == 0) | (master_df['low'] == 0) | (master_df['close'] == 0)
    high_low_mask = master_df['high'] < master_df['low']
    
    report["anomalies"]["nan_values"] = int(nan_mask.sum())
    report["anomalies"]["negative_prices"] = int(neg_mask.sum())
    report["anomalies"]["zero_prices"] = int(zero_mask.sum())
    report["anomalies"]["high_less_than_low"] = int(high_low_mask.sum())
    
    corrupted_mask = nan_mask | neg_mask | zero_mask | high_low_mask
    report["corrupted_rows_removed"] = int(corrupted_mask.sum())
    
    # Remove corrupted
    master_df = master_df[~corrupted_mask].copy()
    
    # Sort and Deduplicate
    master_df.sort_values('timestamp', inplace=True)
    initial_len = len(master_df)
    master_df.drop_duplicates(subset=['timestamp'], keep='first', inplace=True)
    report["duplicates_removed"] = initial_len - len(master_df)
    
    # Gap Analysis
    master_df['time_diff'] = master_df['timestamp'].diff().dt.total_seconds() / 60.0
    
    # Expected gaps: Weekends (typically around 2880 mins = 48 hours)
    weekend_gaps = master_df[master_df['time_diff'] >= 2880]
    # Unexpected gaps: Missing intraday candles
    unexpected_gaps = master_df[(master_df['time_diff'] > 1) & (master_df['time_diff'] < 2880)]
    
    report["gap_analysis"] = {
        "expected_weekend_gaps": len(weekend_gaps),
        "unexpected_intraday_gaps": len(unexpected_gaps),
        "max_gap_duration_mins": float(master_df['time_diff'].max()) if not pd.isna(master_df['time_diff'].max()) else 0
    }
    
    # Cleanup for final output
    master_df.drop(columns=['time_diff'], inplace=True)
    
    # Write canonical dataset
    output_path = r"d:\Gold Scripts\MQL5\Ticks Data\XAUUSD\grid research\apex\data\m1\tmp_EURUSD_M1.csv"
    master_df = master_df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    master_df.to_csv(output_path, index=False, encoding='utf-8')
    
    report["final_dataset"] = {
        "filename": "EURUSD_M1.csv",
        "total_rows": len(master_df),
        "start_date": str(master_df['timestamp'].iloc[0]),
        "end_date": str(master_df['timestamp'].iloc[-1])
    }
    
    # Save report JSON to artifacts
    report_path = r"C:\Users\User10\.gemini\antigravity-ide\brain\1b73ef8e-c034-4d4f-9ea6-ffe8c7aa8368\dataset_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
        
    print(f"Successfully processed {len(master_df)} rows. Saved to tmp_EURUSD_M1.csv")

if __name__ == '__main__':
    build_dataset()
