import os
import pandas as pd
import numpy as np

def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()

def run_study():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'm1', 'EURUSD_M1.parquet'))
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports'))
    
    print(f"Loading M1 data from: {data_path}")
    df = pd.read_parquet(data_path)
    
    print("Calculating ATR...")
    df['atr_14'] = calculate_atr(df, 14)
    
    print("Constructing 15-bar non-overlapping blocks...")
    # Extract rows at 15-bar intervals. We need to measure over the preceding 15 bars.
    # e.g., if we take idx 15, 30, 45...
    # For a block ending at idx, it spans [idx-14 : idx] (15 bars inclusive).
    # Since we need shift(-15) for return, we just take df.iloc[15::15].copy()
    # But to compute 15-bar High/Low, we need rolling over the M1 frame first.
    
    df['block_high_15'] = df['high'].rolling(15).max()
    df['block_low_15'] = df['low'].rolling(15).min()
    df['block_range_15'] = df['block_high_15'] - df['block_low_15']
    df['block_ret_15'] = df['close'] - df['close'].shift(15)
    
    # Forward outcomes (on M1 frame, then sampled)
    indexer_60 = pd.api.indexers.FixedForwardWindowIndexer(window_size=60)
    df['fwd_high_60'] = df['high'].shift(-1).rolling(window=indexer_60).max()
    df['fwd_low_60'] = df['low'].shift(-1).rolling(window=indexer_60).min()
    df['fwd_close_60'] = df['close'].shift(-60)
    
    indexer_240 = pd.api.indexers.FixedForwardWindowIndexer(window_size=240)
    df['fwd_high_240'] = df['high'].shift(-1).rolling(window=indexer_240).max()
    df['fwd_low_240'] = df['low'].shift(-1).rolling(window=indexer_240).min()
    df['fwd_close_240'] = df['close'].shift(-240)
    
    print("Extracting blocks...")
    # Start from index 15 to ensure we have a full first block
    blocks = df.iloc[15::15].copy().reset_index()
    
    # Need ATR at start of block for normalization
    # If block ends at idx, it started at idx-15
    # Since blocks is sampled at idx, we can just use shift(1) of the block dataframe!
    blocks['start_atr'] = blocks['atr_14'].shift(1)
    
    print("Computing State Dimensions...")
    # Volatility State: 1-week is 5 days * 24h * 4 blocks/h = 480 blocks
    blocks['vol_pct_25'] = blocks['block_range_15'].rolling(480).quantile(0.25)
    blocks['vol_pct_75'] = blocks['block_range_15'].rolling(480).quantile(0.75)
    
    def get_vol_state(row):
        if pd.isna(row['vol_pct_25']): return None
        if row['block_range_15'] < row['vol_pct_25']: return 'LOW_VOL'
        if row['block_range_15'] > row['vol_pct_75']: return 'HIGH_VOL'
        return 'NORMAL_VOL'
        
    blocks['vol_state'] = blocks.apply(get_vol_state, axis=1)
    
    # Directional State
    blocks['norm_ret'] = blocks['block_ret_15'] / (blocks['start_atr'] + 1e-9)
    
    def get_dir_state(row):
        if pd.isna(row['norm_ret']): return None
        if row['norm_ret'] > 1.0: return 'BULL'
        if row['norm_ret'] < -1.0: return 'BEAR'
        return 'FLAT'
        
    blocks['dir_state'] = blocks.apply(get_dir_state, axis=1)
    
    # Composite State
    blocks['state'] = blocks['vol_state'] + '_' + blocks['dir_state']
    
    # Filter out initial NaNs
    blocks = blocks.dropna(subset=['state']).copy()
    blocks = blocks[blocks['state'].str.contains('None') == False].copy()
    blocks.reset_index(drop=True, inplace=True)
    
    print(f"Total valid non-overlapping blocks: {len(blocks)}")
    
    # Compute Outcomes for blocks
    blocks['ret_60'] = blocks['fwd_close_60'] - blocks['close']
    blocks['ret_240'] = blocks['fwd_close_240'] - blocks['close']
    blocks['mfe_60'] = blocks['fwd_high_60'] - blocks['close']
    blocks['mae_60'] = blocks['close'] - blocks['fwd_low_60']
    
    print("Constructing Sequences...")
    # N=3 Sequence
    blocks['seq_3'] = blocks['state'].shift(2) + ' -> ' + blocks['state'].shift(1) + ' -> ' + blocks['state']
    # N=5 Sequence
    blocks['seq_5'] = blocks['state'].shift(4) + ' -> ' + blocks['state'].shift(3) + ' -> ' + blocks['state'].shift(2) + ' -> ' + blocks['state'].shift(1) + ' -> ' + blocks['state']
    
    # Drop rows where sequences haven't fully formed or at the very end where outcomes are NaN
    valid_blocks = blocks.dropna(subset=['seq_5', 'fwd_close_240']).copy()
    
    print("Saving Dataset...")
    valid_blocks.to_parquet(os.path.join(reports_dir, "RC009_Study_003_Sequence_Dataset.parquet"), index=False)
    
    print("Generating Baselines...")
    # Baseline A: All valid blocks
    baseline_a = valid_blocks[['ret_60', 'ret_240', 'mfe_60', 'mae_60']].copy()
    
    # For Baselines B and C, they are dynamic per final state. We will compute them 
    # dynamically in the analysis script by grouping `valid_blocks`.
    # Just need to make sure the dataset is saved.
    
    print("Study 003 extraction complete.")

if __name__ == "__main__":
    run_study()
