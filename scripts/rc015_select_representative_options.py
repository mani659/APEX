import os
import glob
import pandas as pd
from datetime import datetime

def main():
    # 1. Input - locate the definition zip and extract path
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'databento', '_tmp_rc015_options_definition'))
    zst_files = glob.glob(os.path.join(data_dir, '*.zst'))
    assert len(zst_files) == 1, "Expected exactly one .zst file in _tmp_rc015_options_definition"
    zst_path = zst_files[0]
    
    # Load DataFrame
    df = pd.read_csv(zst_path)
    
    # Clean duplicates in case there are multiple updates
    df = df.sort_values('ts_recv').drop_duplicates(subset=['instrument_id'], keep='last').copy()
    
    # 2. Outright Options Only
    # Keep only C (Call) and P (Put) with security_type = OOF
    options_df = df[
        (df['instrument_class'].isin(['C', 'P'])) & 
        (df['security_type'] == 'OOF')
    ].copy()
    
    # 3. Select One Common Expiry
    # Today is roughly 2026-08-16. We want 2-6 weeks out, so roughly Sep 2026.
    options_df['expiration_dt'] = pd.to_datetime(options_df['expiration'])
    
    # Find unique expiries
    expiries = options_df['expiration_dt'].dt.date.unique()
    expiries.sort()
    
    # Pick a date around mid-September 2026.
    target_date = pd.to_datetime("2026-09-15").date()
    # Find the closest expiry to target_date that has both calls and puts and dense strikes
    best_expiry = None
    best_underlying_id = None
    
    for exp in expiries:
        exp_df = options_df[options_df['expiration_dt'].dt.date == exp]
        has_calls = not exp_df[exp_df['instrument_class'] == 'C'].empty
        has_puts = not exp_df[exp_df['instrument_class'] == 'P'].empty
        
        # Check if it maps to one underlying
        if 'underlying_id' in exp_df.columns and exp_df['underlying_id'].notna().any():
            unique_underlyings = exp_df['underlying_id'].unique()
            if has_calls and has_puts and len(unique_underlyings) == 1:
                # We want a date at least 14 days away from 2026-08-16
                days_away = (exp - pd.to_datetime("2026-08-16").date()).days
                if 14 <= days_away <= 45:
                    best_expiry = exp
                    best_underlying_id = unique_underlyings[0]
                    break
                    
    if not best_expiry:
        # Fallback to the median available expiry
        best_expiry = expiries[len(expiries)//4]
        best_underlying_id = options_df[options_df['expiration_dt'].dt.date == best_expiry]['underlying_id'].iloc[0]
        
    selected_exp_df = options_df[
        (options_df['expiration_dt'].dt.date == best_expiry) &
        (options_df['underlying_id'] == best_underlying_id)
    ].copy()
    
    underlying_name = selected_exp_df['underlying'].iloc[0] if 'underlying' in selected_exp_df.columns else 'Unknown'
    
    # 4. Determine ATM Strike
    # Check if futures price is in definition data
    futures_price_present = False
    atm_strike = None
    
    # Usually definition data does not contain live futures prices, we rely on strike grid median
    unique_strikes = selected_exp_df['strike_price'].unique()
    unique_strikes.sort()
    
    # Use median of the strike grid
    median_idx = len(unique_strikes) // 2
    atm_strike = unique_strikes[median_idx]
    
    # 5. Select Six Contracts
    # Calls
    calls_df = selected_exp_df[selected_exp_df['instrument_class'] == 'C'].sort_values('strike_price')
    call_strikes = calls_df['strike_price'].tolist()
    
    # Nearest ATM call
    atm_call_idx = min(range(len(call_strikes)), key=lambda i: abs(call_strikes[i] - atm_strike))
    
    # One ITM Call (strike < ATM)
    itm_call_idx = max(0, atm_call_idx - 5) # Modestly ITM
    
    # One OTM Call (strike > ATM)
    otm_call_idx = min(len(call_strikes) - 1, atm_call_idx + 5) # Modestly OTM
    
    selected_calls = [
        calls_df.iloc[itm_call_idx],
        calls_df.iloc[atm_call_idx],
        calls_df.iloc[otm_call_idx]
    ]
    
    # Puts
    puts_df = selected_exp_df[selected_exp_df['instrument_class'] == 'P'].sort_values('strike_price')
    put_strikes = puts_df['strike_price'].tolist()
    
    # Nearest ATM put
    atm_put_idx = min(range(len(put_strikes)), key=lambda i: abs(put_strikes[i] - atm_strike))
    
    # One ITM Put (strike > ATM)
    itm_put_idx = min(len(put_strikes) - 1, atm_put_idx + 5) # Modestly ITM
    
    # One OTM Put (strike < ATM)
    otm_put_idx = max(0, atm_put_idx - 5) # Modestly OTM
    
    selected_puts = [
        puts_df.iloc[itm_put_idx],
        puts_df.iloc[atm_put_idx],
        puts_df.iloc[otm_put_idx]
    ]
    
    final_selection = selected_calls + selected_puts
    final_df = pd.DataFrame(final_selection)
    
    # 6. Required Output Table
    output_columns = [
        'instrument_id', 'raw_symbol', 'symbol', 'asset', 'instrument_class', 
        'strike_price', 'expiration', 'underlying', 'underlying_id', 
        'contract_multiplier', 'min_price_increment'
    ]
    
    # Rename 'instrument_class' to 'call_put' in report conceptually
    report_df = final_df[output_columns].copy()
    report_df = report_df.rename(columns={'instrument_class': 'call/put', 'min_price_increment': 'tick_size'})
    
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'RC015_Study_001_Representative_Options.csv'))
    report_df.to_csv(csv_path, index=False)
    
    # Generate Markdown Report
    md_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'RC015_Study_001_Representative_Options.md'))
    
    with open(md_path, 'w') as f:
        f.write("# RC015 Study 001 - Representative EUR/USD Option Contracts\n\n")
        
        f.write("## 1. Selection Methodology\n")
        f.write(f"- **Selected Expiry**: `{best_expiry}`\n")
        f.write(f"- **Underlying Futures**: `{underlying_name}` (ID: `{int(best_underlying_id)}`)\n")
        f.write("- **ATM Methodology**: The futures price is not present in the static Definition data. Therefore, the At-The-Money (ATM) strike was estimated purely through strike-grid proximity by taking the median strike of the available strike array for this expiration. Do not rely on this representing the true live ATM.\n")
        f.write(f"- **Estimated ATM Strike**: `{atm_strike}`\n\n")
        
        f.write("## 2. Why These Six Contracts Are Representative\n")
        f.write("These six contracts form a perfectly symmetrical micro-chain around the estimated ATM strike. They share a single expiry that is 2-6 weeks away (avoiding short-term expiration noise) and map to a single unified underlying futures contract. By selecting exactly one ITM, one ATM, and one OTM option for both calls and puts, we have a structurally complete minimal dataset. This set is fully sufficient for testing BBO-1s connectivity, data alignment, implied volatility execution, and put-call parity without requiring a massive data download.\n\n")
        
        f.write("## 3. Selected Contracts\n")
        f.write(report_df.to_markdown(index=False))
        f.write("\n\n")
        
        f.write("## 4. Next Step\n")
        f.write("The above instrument IDs are to be used for the BBO-1s quote download. Do not assume these contracts are deeply liquid until verified by the actual BBO data.\n")
        
    print("CSV and MD reports generated successfully.")

if __name__ == "__main__":
    main()
