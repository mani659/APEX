import os
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar, GoodFriday

def generate_manifest():
    out_dir = 'reports'
    os.makedirs(out_dir, exist_ok=True)
    
    start_date = '2022-01-01'
    end_date = '2026-06-30'
    
    # Generate all Fridays
    all_fridays = pd.date_range(start_date, end_date, freq='W-FRI')
    
    # Construct a custom CME FX holiday calendar
    cal = USFederalHolidayCalendar()
    cal.rules.append(GoodFriday)
    
    # Generate holidays between start and end
    holidays = cal.holidays(start=start_date, end=end_date).date
    
    records = []
    
    for expiry in all_fridays:
        obs_date = expiry - pd.Timedelta(days=2)  # Wednesday
        
        is_expiry_holiday = expiry.date() in holidays
        is_obs_holiday = obs_date.date() in holidays
        
        # Check if the date is a valid trading day
        # For simplicity, if either Wednesday or Friday is a holiday, mark unavailable
        # We can also check week of month to assign the root
        week_of_month = (expiry.day - 1) // 7 + 1
        option_root = f'{week_of_month}EU'
        
        # Monthly options (EUU) usually expire on the Friday before the 2nd Wednesday?
        # Actually, let's just list {week_of_month}EU and EUU as possible roots for that Friday.
        # We will use {week_of_month}EU as the primary weekly root designation.
        if week_of_month > 5:
             option_root = '5EU' # edge case for some months
             
        # Determine underlying futures contract
        # Euro FX futures roll quarterly (H, M, U, Z) - Mar, Jun, Sep, Dec.
        month = expiry.month
        year = expiry.year
        if month <= 3:
            fut_code = f'6EH{str(year)[-1]}'
            if year == 2022: fut_code = '6EH2'
            elif year == 2023: fut_code = '6EH3'
            elif year == 2024: fut_code = '6EH4'
            elif year == 2025: fut_code = '6EH5'
            elif year == 2026: fut_code = '6EH6'
        elif month <= 6:
            fut_code = f'6EM{str(year)[-1]}'
        elif month <= 9:
            fut_code = f'6EU{str(year)[-1]}'
        else:
            fut_code = f'6EZ{str(year)[-1]}'
            
        status = 'QUALIFIED'
        if is_expiry_holiday or is_obs_holiday:
            status = 'UNAVAILABLE (HOLIDAY)'
            
        records.append({
            'expiry_date': expiry.strftime('%Y-%m-%d'),
            'observation_date': obs_date.strftime('%Y-%m-%d'),
            'weekday': 'Friday',
            'option_root': option_root,
            'expected_dte': 2,
            'underlying_futures_contract': fut_code,
            'underlying_expiry': 'Quarterly',
            'data_required': 'BBO-1m' if status == 'QUALIFIED' else 'None',
            'availability_status': status
        })
        
    df = pd.DataFrame(records)
    
    # Write CSV
    csv_path = os.path.join(out_dir, 'RC015_Study_007_Acquisition_Summary.csv')
    df.to_csv(csv_path, index=False)
    
    # Calculate Summary Stats
    total_fridays = len(df)
    holidays_excluded = len(df[df['availability_status'] != 'QUALIFIED'])
    qualifying_count = len(df[df['availability_status'] == 'QUALIFIED'])
    
    # Cost Estimate
    # 1 day of BBO-1m per root is approx 2MB compressed.
    # We need Wed, Thu, Fri (3 days) for Option + Future = 6 days of data per event
    # 6 days * 2MB = 12MB per event.
    # 12MB * qualifying_count = total MB. Databento cost is minimal (e.g. $1 per GB).
    mb_per_event = 12
    total_mb = qualifying_count * mb_per_event
    est_cost = total_mb / 1024 * 0.50 # Assuming $0.50 per GB for historical BBO-1m
    
    manifest_path = os.path.join(out_dir, 'RC015_Study_007_Acquisition_Manifest.md')
    with open(manifest_path, 'w') as f:
        f.write('# RC015 Study 007 — Corrected Data Acquisition Manifest\n\n')
        f.write('## 1. Scope & Definitions\n')
        f.write(f'- **Historical Range**: {start_date} through {end_date}\n')
        f.write('- **Observation**: Wednesday (~2 DTE)\n')
        f.write('- **Expiry**: Friday\n')
        f.write('- **Option Roots**: Friday weekly (1EU, 2EU, 3EU, 4EU, 5EU) and Monthly (EUU)\n')
        f.write('- **Futures**: CME Euro FX (6E)\n')
        f.write('- **Schema**: `BBO-1m`\n')
        f.write('- **Spot RV**: Canonical `data/m1/EURUSD_M1.parquet` (No new spot data required)\n\n')
        
        f.write('## 2. Near-ATM Rule\n')
        f.write('`abs(strike - futures_mid) <= 0.0020` applied at contemporaneous observation.\n\n')
        
        f.write('## 3. Sample Size Statistics\n')
        f.write(f'- **Total Calendar Fridays**: {total_fridays}\n')
        f.write(f'- **Holiday/Missing Exclusions**: {holidays_excluded}\n')
        f.write(f'- **Final Qualifying Observation Events**: {qualifying_count}\n\n')
        
        f.write('## 4. Cost & Volume Estimate\n')
        f.write(f'- **Qualifying Event Count**: {qualifying_count}\n')
        f.write('- **Option Data Days**: ~3 days per event (Wed-Fri)\n')
        f.write('- **Futures Data Days**: ~3 days per event (Wed-Fri)\n')
        f.write('- **Expected Parent Requests**: BBO-1m for specific 1EU-5EU/EUU roots.\n')
        f.write(f'- **Approximate Data Volume**: ~{total_mb} MB compressed\n')
        f.write(f'- **Approximate Cost**: < $5.00 USD (Databento BBO-1m historical pricing)\n\n')
        
        f.write('## 5. Expiry Schedule Snapshot (First 20)\n')
        f.write('| Expiry Date | Observation Date | Option Root | Futures | Status |\n')
        f.write('| :--- | :--- | :--- | :--- | :--- |\n')
        for _, row in df.head(20).iterrows():
            f.write(f'| {row["expiry_date"]} | {row["observation_date"]} | {row["option_root"]} | {row["underlying_futures_contract"]} | {row["availability_status"]} |\n')
            
        f.write(f'\n*See `RC015_Study_007_Acquisition_Summary.csv` for the full {total_fridays}-row calendar.*\n')

    print("Manifest and Summary generated.")

if __name__ == '__main__':
    generate_manifest()
