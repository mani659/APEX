import os
import pandas as pd
import numpy as np

def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()

def run_discovery():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'm1', 'EURUSD_M1.parquet'))
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports'))
    os.makedirs(reports_dir, exist_ok=True)
    
    print(f"Loading M1 data from: {data_path}")
    df = pd.read_parquet(data_path)
    
    print("Calculating rolling metrics (This may take a moment)...")
    df['atr_14'] = calculate_atr(df, 14)
    df['range'] = df['high'] - df['low']
    df['body'] = np.abs(df['close'] - df['open'])
    df['is_bullish'] = df['close'] > df['open']
    
    # Pre-calculate 1-week (7200 bars) rolling percentiles
    print("Calculating rolling percentiles for Volume and Volatility...")
    # Rolling rank is slow in pandas, we'll use a fast rolling quantile approximation or rolling min/max for speed
    # To exact rolling quantile on 2M rows is very slow. 
    # We will use Z-score as a robust and fast proxy for percentiles.
    # 95th percentile ~ Z > 1.645
    # 5th percentile ~ Z < -1.645
    # 25th percentile ~ Z < -0.67
    
    df['vol_mean_7200'] = df['volume'].rolling(7200).mean()
    df['vol_std_7200'] = df['volume'].rolling(7200).std()
    df['volume_z'] = (df['volume'] - df['vol_mean_7200']) / (df['vol_std_7200'] + 1e-9)
    
    # 60-bar historical volatility (measured as std of close)
    df['hist_vol_60'] = df['close'].rolling(60).std()
    df['hist_vol_mean_7200'] = df['hist_vol_60'].rolling(7200).mean()
    df['hist_vol_std_7200'] = df['hist_vol_60'].rolling(7200).std()
    df['hist_vol_z'] = (df['hist_vol_60'] - df['hist_vol_mean_7200']) / (df['hist_vol_std_7200'] + 1e-9)
    
    print("Computing Forward Outcomes...")
    # Calculate MFE/MAE for Long over next 60 and 240 bars
    # This requires rolling max/min on future shifted data
    
    # Shift backwards to align future prices to current row
    # Forward 60
    indexer_60 = pd.api.indexers.FixedForwardWindowIndexer(window_size=60)
    df['fwd_high_60'] = df['high'].shift(-1).rolling(window=indexer_60).max()
    df['fwd_low_60'] = df['low'].shift(-1).rolling(window=indexer_60).min()
    df['fwd_close_60'] = df['close'].shift(-60)
    
    # Forward 240
    indexer_240 = pd.api.indexers.FixedForwardWindowIndexer(window_size=240)
    df['fwd_high_240'] = df['high'].shift(-1).rolling(window=indexer_240).max()
    df['fwd_low_240'] = df['low'].shift(-1).rolling(window=indexer_240).min()
    df['fwd_close_240'] = df['close'].shift(-240)
    
    print("Evaluating Candidate 1: Volatility Compression Squeeze")
    # Z < -1.645 is approx 5th percentile
    cond_compression = df['hist_vol_z'].shift(1) < -1.645
    cond_breakout = df['range'] > (2.0 * df['atr_14'].shift(1))
    c1_mask = cond_compression & cond_breakout
    
    c1_events = []
    for idx in np.where(c1_mask)[0]:
        if idx >= len(df) - 240: continue
        direction = "LONG" if df['is_bullish'].iloc[idx] else "SHORT"
        c1_events.append({"idx": idx, "candidate": "C1_Squeeze", "direction": direction})
        
    print("Evaluating Candidate 2: Participation/Price Divergence (Absorption)")
    # Volume Z > 1.645 (95th pct), Body < 20% Range, Range < 1.0 ATR
    cond_high_vol = df['volume_z'] > 1.645
    cond_small_body = df['body'] < (0.2 * df['range'])
    cond_small_range = df['range'] < df['atr_14'].shift(1)
    c2_mask = cond_high_vol & cond_small_body & cond_small_range
    
    c2_events = []
    for idx in np.where(c2_mask)[0]:
        if idx >= len(df) - 240: continue
        # Reversal direction: if it was bullish, we expect short.
        direction = "SHORT" if df['is_bullish'].iloc[idx] else "LONG"
        c2_events.append({"idx": idx, "candidate": "C2_Absorption", "direction": direction})
        
    print("Evaluating Candidate 3: Momentum Ignition")
    # 3 bars same direction, increasing body, increasing volume
    c3_mask_long = (df['is_bullish'] & (df['is_bullish'].shift(1) == True) & (df['is_bullish'].shift(2) == True)) & \
                   (df['body'] > df['body'].shift(1)) & (df['body'].shift(1) > df['body'].shift(2)) & \
                   (df['volume'] > df['volume'].shift(1)) & (df['volume'].shift(1) > df['volume'].shift(2))
    
    c3_mask_short = (~df['is_bullish'] & (df['is_bullish'].shift(1) == False) & (df['is_bullish'].shift(2) == False)) & \
                    (df['body'] > df['body'].shift(1)) & (df['body'].shift(1) > df['body'].shift(2)) & \
                    (df['volume'] > df['volume'].shift(1)) & (df['volume'].shift(1) > df['volume'].shift(2))
                    
    c3_events = []
    for idx in np.where(c3_mask_long)[0]:
        if idx < len(df) - 240: c3_events.append({"idx": idx, "candidate": "C3_Ignition", "direction": "LONG"})
    for idx in np.where(c3_mask_short)[0]:
        if idx < len(df) - 240: c3_events.append({"idx": idx, "candidate": "C3_Ignition", "direction": "SHORT"})
        
    print("Evaluating Candidate 4: Low-Participation Pullback (Flag)")
    # 60-bar trend > 2.0 ATR, followed by 15 bars vol_z < -0.67 and total move < 0.5 ATR
    df['trend_60'] = df['close'] - df['close'].shift(60)
    df['trend_mag_60'] = np.abs(df['trend_60']) / df['atr_14'].shift(60)
    
    df['max_vol_z_15'] = df['volume_z'].rolling(15).max()
    df['price_move_15'] = np.abs(df['close'] - df['close'].shift(15)) / df['atr_14'].shift(15)
    
    # A flag requires the preceding 60-bar trend (shifted 15 bars ago) to be > 2.0 ATR
    cond_strong_trend = df['trend_mag_60'].shift(15) > 2.0
    cond_low_vol = df['max_vol_z_15'] < -0.67
    cond_tight_price = df['price_move_15'] < 0.5
    
    c4_mask = cond_strong_trend & cond_low_vol & cond_tight_price
    
    c4_events = []
    for idx in np.where(c4_mask)[0]:
        if idx >= len(df) - 240: continue
        # Direction is the same as the underlying 60-bar trend 15 bars ago
        trend_val = df['trend_60'].iloc[idx - 15]
        direction = "LONG" if trend_val > 0 else "SHORT"
        c4_events.append({"idx": idx, "candidate": "C4_Flag", "direction": direction})
        
    print(f"Events Found -> C1: {len(c1_events)}, C2: {len(c2_events)}, C3: {len(c3_events)}, C4: {len(c4_events)}")
    
    all_events = c1_events + c2_events + c3_events + c4_events
    
    # Calculate Outcomes for all events
    records = []
    
    # Baseline C: Matched Control (1440 bars prior)
    control_records = []
    
    for ev in all_events:
        idx = ev["idx"]
        candidate = ev["candidate"]
        direction = ev["direction"]
        
        row = df.iloc[idx]
        entry = row['close']
        
        # Calculate Returns
        ret_60 = row['fwd_close_60'] - entry
        ret_240 = row['fwd_close_240'] - entry
        mfe_60 = row['fwd_high_60'] - entry
        mae_60 = entry - row['fwd_low_60']
        
        if direction == "SHORT":
            ret_60 = -ret_60
            ret_240 = -ret_240
            temp = mfe_60
            mfe_60 = mae_60
            mae_60 = temp # MAE is always positive adverse excursion
            
        records.append({
            "idx": idx,
            "candidate": candidate,
            "direction": direction,
            "ret_60": ret_60,
            "ret_240": ret_240,
            "mfe_60": mfe_60,
            "mae_60": mae_60
        })
        
        # Generate Control
        ctrl_idx = idx - 1440
        if ctrl_idx >= 0:
            crow = df.iloc[ctrl_idx]
            centry = crow['close']
            cret_60 = crow['fwd_close_60'] - centry
            cret_240 = crow['fwd_close_240'] - centry
            cmfe_60 = crow['fwd_high_60'] - centry
            cmae_60 = centry - crow['fwd_low_60']
            
            if direction == "SHORT":
                cret_60 = -cret_60
                cret_240 = -cret_240
                ctemp = cmfe_60
                cmfe_60 = cmae_60
                cmae_60 = ctemp
                
            control_records.append({
                "idx": ctrl_idx,
                "candidate": f"{candidate}_Control",
                "direction": direction,
                "ret_60": cret_60,
                "ret_240": cret_240,
                "mfe_60": cmfe_60,
                "mae_60": cmae_60
            })
            
    df_events = pd.DataFrame(records)
    df_events.to_parquet(os.path.join(reports_dir, "RC009_Discovery_Dataset.parquet"), index=False)
    
    df_control = pd.DataFrame(control_records)
    df_control.to_parquet(os.path.join(reports_dir, "RC009_Control_Dataset.parquet"), index=False)
    
    # Compute Unconditional Baselines (Sample randomly to keep manageable, 100k samples)
    np.random.seed(42)
    sample_indices = np.random.choice(len(df) - 240, 100000, replace=False)
    
    baseline_records = []
    for idx in sample_indices:
        # 50% long, 50% short for symmetrical baseline
        direction = "LONG" if np.random.rand() > 0.5 else "SHORT"
        row = df.iloc[idx]
        entry = row['close']
        
        ret_60 = row['fwd_close_60'] - entry
        ret_240 = row['fwd_close_240'] - entry
        mfe_60 = row['fwd_high_60'] - entry
        mae_60 = entry - row['fwd_low_60']
        
        if direction == "SHORT":
            ret_60 = -ret_60
            ret_240 = -ret_240
            temp = mfe_60
            mfe_60 = mae_60
            mae_60 = temp
            
        baseline_records.append({
            "idx": idx,
            "direction": direction,
            "ret_60": ret_60,
            "ret_240": ret_240,
            "mfe_60": mfe_60,
            "mae_60": mae_60
        })
        
    df_baseline = pd.DataFrame(baseline_records)
    df_baseline.to_parquet(os.path.join(reports_dir, "RC009_Baseline_Dataset.parquet"), index=False)
    
    print("All datasets generated successfully.")

if __name__ == "__main__":
    run_discovery()
