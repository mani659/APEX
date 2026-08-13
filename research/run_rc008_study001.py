import os
import pandas as pd
import numpy as np

def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()

def run_context_extraction():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'm1', 'EURUSD_M1.parquet'))
    events_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'RC007_Study_009_Exit_Distribution.parquet'))
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'RC008_Context_Dataset.parquet'))
    
    print(f"Loading M1 data from: {data_path}")
    df = pd.read_parquet(data_path)
    
    time_col = [c for c in df.columns if 'time' in c.lower()][0]
    df['timestamp'] = pd.to_datetime(df[time_col])
    
    print("Calculating ATR...")
    df['atr_14'] = calculate_atr(df, 14)
    
    print("Calculating Volatility Context (1-Week Percentile)...")
    # 5 trading days * 24 hours * 60 minutes = 7200 bars
    df['atr_7200_max'] = df['atr_14'].rolling(7200).max()
    df['atr_7200_min'] = df['atr_14'].rolling(7200).min()
    df['vol_pct'] = (df['atr_14'] - df['atr_7200_min']) / (df['atr_7200_max'] - df['atr_7200_min'] + 1e-9)
    
    print("Calculating Trend Context...")
    df['ma_1440'] = df['close'].rolling(1440).mean()
    df['dist_1440'] = (df['close'] - df['ma_1440']) / df['atr_14']
    df['ret_240'] = (df['close'] - df['close'].shift(240)) / df['atr_14']
    
    print("Calculating Liquidity Context...")
    df['vol_mean_240'] = df['volume'].rolling(240).mean()
    df['vol_std_240'] = df['volume'].rolling(240).std()
    df['volume_z'] = (df['volume'] - df['vol_mean_240']) / (df['vol_std_240'] + 1e-9)
    
    print("Calculating Path Context (60-bar Momentum)...")
    df['mom_60'] = (df['close'] - df['close'].shift(60)) / df['atr_14']
    
    print("Calculating Temporal Context...")
    df['hour'] = df['timestamp'].dt.hour
    
    print("Loading Events...")
    events_df = pd.read_parquet(events_path)
    
    # We should ensure both are datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    events_df['timestamp'] = pd.to_datetime(events_df['timestamp'])
    
    print(f"Merging {len(events_df)} events with context dataset...")
    
    # We must grab the context strictly from the bar *before* the execution bar, 
    # or the execution bar itself since execution happens at the open of the bar, 
    # meaning the close of the PREVIOUS bar contains all the pre-event information.
    # To be absolutely sure there is no lookahead bias, we will shift all context columns by 1!
    
    context_cols = ['atr_14', 'vol_pct', 'dist_1440', 'ret_240', 'volume_z', 'mom_60', 'hour']
    for col in context_cols:
        df[col] = df[col].shift(1)
        
    merged = pd.merge(events_df, df[['timestamp'] + context_cols], on='timestamp', how='left')
    
    print(f"Dataset compiled. Rows: {len(merged)}")
    
    # Define favorable / unfavorable label
    # Favorable = profit > 0 in isolated model 1
    merged['is_favorable'] = (merged['m1_pnl'] > 0).astype(int)
    
    merged.to_parquet(out_path, index=False)
    print(f"Saved to: {out_path}")

if __name__ == "__main__":
    run_context_extraction()
