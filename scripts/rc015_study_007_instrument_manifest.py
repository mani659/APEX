import os
import sys
import pandas as pd
import databento as db
import concurrent.futures
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

def process_event(idx, row, api_key):
    client = db.Historical(api_key)
    obs_date_str = row['observation_date']
    exp_date_str = row['expiry_date']
    event_id = f"{obs_date_str}_{exp_date_str}"
    
    fut_res = None
    opt_res = []
    
    # Trackers for this event
    has_bbo_data = False
    has_opt_def_data = False
    symbology_errors = 0
    missing_market_data = 0
    coverage_gaps = 0
    no_matching_expiry = False
    
    # 1. Futures Definition
    try:
        fut_def = client.timeseries.get_range(
            dataset='GLBX.MDP3',
            symbols='6E.FUT',
            stype_in='parent',
            schema='definition',
            start=f"{obs_date_str}T00:00:00",
            end=f"{obs_date_str}T23:59:59"
        ).to_df()
        
        fut_def['expiration'] = pd.to_datetime(fut_def['expiration'])
        active_futs = fut_def[(fut_def['expiration'].dt.date > pd.to_datetime(obs_date_str).date()) & (fut_def['instrument_class'] == 'F')]
        if active_futs.empty:
            return event_id, None, [], {"bbo_missing": False, "symbology_err": False, "coverage_gaps": 0, "missing_data": 1, "no_expiry": False}
        
        active_fut = active_futs.sort_values('expiration').iloc[0]
        fut_instrument_id = active_fut['instrument_id']
        fut_symbol = active_fut['symbol']
    except Exception as e:
        err_msg = str(e).lower()
        if '422' in err_msg or 'symbology' in err_msg or '400' in err_msg:
            return event_id, None, [], {"bbo_missing": False, "symbology_err": True, "coverage_gaps": 0, "missing_data": 0, "no_expiry": False}
        return event_id, None, [], {"bbo_missing": False, "symbology_err": False, "coverage_gaps": 0, "missing_data": 1, "no_expiry": False}
        
    fut_res = {
        'event_id': event_id,
        'observation_date': obs_date_str,
        'expiry_date': exp_date_str,
        'futures_instrument_id': fut_instrument_id,
        'futures_symbol': fut_symbol,
        'status': 'QUALIFIED'
    }

    # 2. Option Definition using correct parents
    valid_opts = pd.DataFrame()
    option_parents = ['EUU.OPT', '1EU.OPT', '2EU.OPT', '3EU.OPT', '4EU.OPT', '5EU.OPT']
    
    try:
        opt_def = client.timeseries.get_range(
            dataset='GLBX.MDP3',
            symbols=option_parents,
            stype_in='parent',
            schema='definition',
            start=f"{obs_date_str}T00:00:00",
            end=f"{obs_date_str}T23:59:59"
        ).to_df()
        
        if not opt_def.empty:
            has_opt_def_data = True
            opt_def['expiration'] = pd.to_datetime(opt_def['expiration'])
            target_exp = pd.to_datetime(exp_date_str).date()
            
            # Find matching expiries, class, security_type, and underlying
            valid_opts = opt_def[
                (opt_def['expiration'].dt.date == target_exp) &
                (opt_def['instrument_class'].isin(['C', 'P'])) &
                (opt_def['security_type'] == 'OOF') &
                (opt_def['underlying_id'] == fut_instrument_id) &
                (opt_def['strike_price'] > 0)
            ].copy()
            
            if valid_opts.empty:
                no_matching_expiry = True
                
    except Exception as e:
        err_msg = str(e).lower()
        if '422' in err_msg or 'symbology' in err_msg or '400' in err_msg:
            symbology_errors += 1
        else:
            missing_market_data += 1

    # 3. Futures BBO-1m
    bbo_missing = False
    try:
        fut_bbo = client.timeseries.get_range(
            dataset='GLBX.MDP3',
            symbols=[fut_instrument_id],
            stype_in='instrument_id',
            schema='bbo-1m',
            start=f"{obs_date_str}T00:00:00",
            end=f"{obs_date_str}T23:59:59"
        ).to_df()
        
        if fut_bbo.empty:
            bbo_missing = True
        else:
            fut_bbo = fut_bbo[(fut_bbo['bid_px_00'] > 0) & (fut_bbo['ask_px_00'] > 0)]
            if fut_bbo.empty:
                bbo_missing = True
            else:
                has_bbo_data = True
                
    except Exception as e:
        err_msg = str(e).lower()
        if '422' in err_msg or 'symbology' in err_msg or '400' in err_msg:
            symbology_errors += 1
        else:
            bbo_missing = True

    # 4. Strike Selection over M15 schedule
    valid_obs_count = 0
    if has_bbo_data and not valid_opts.empty:
        # Create M15 schedule for the day
        m15_times = pd.date_range(f"{obs_date_str}T00:00:00", f"{obs_date_str}T23:45:00", freq='15min', tz='UTC')
        
        if not pd.api.types.is_datetime64_any_dtype(fut_bbo.index):
            fut_bbo.index = pd.to_datetime(fut_bbo.index, utc=True)
            
        for obs_ts in m15_times:
            valid_quotes = fut_bbo[fut_bbo.index <= obs_ts]
            if valid_quotes.empty:
                coverage_gaps += 1
                continue
                
            latest_quote = valid_quotes.iloc[-1]
            futures_mid = (latest_quote['bid_px_00'] + latest_quote['ask_px_00']) / 2.0
            
            # Select strikes based on exact contemporaneous midpoint
            valid_opts['moneyness_distance'] = (valid_opts['strike_price'].astype(float) - futures_mid).abs()
            eligible_opts = valid_opts[valid_opts['moneyness_distance'] <= 0.0020]
            
            if not eligible_opts.empty:
                valid_obs_count += 1
                for _, opt in eligible_opts.iterrows():
                    # Deduce parent
                    parent = f"{opt['asset']}.OPT" if pd.notnull(opt.get('asset')) else 'UNKNOWN'
                    
                    opt_res.append({
                        'event_id': event_id,
                        'observation_timestamp': obs_ts.isoformat(),
                        'expiry_date': exp_date_str,
                        'option_parent': parent,
                        'asset': opt['asset'],
                        'instrument_id': opt['instrument_id'],
                        'symbol': opt['symbol'],
                        'raw_symbol': opt['raw_symbol'],
                        'option_type': opt['instrument_class'],
                        'strike': opt['strike_price'],
                        'futures_mid': futures_mid,
                        'moneyness_distance': opt['moneyness_distance'],
                        'underlying_id': opt['underlying_id'],
                        'underlying_symbol': fut_symbol,
                        'security_type': opt['security_type'],
                        'instrument_class': opt['instrument_class'],
                        'status': 'QUALIFIED'
                    })

    metrics = {
        "bbo_missing": bbo_missing,
        "symbology_err": symbology_errors > 0,
        "coverage_gaps": coverage_gaps,
        "missing_data": missing_market_data,
        "no_expiry": no_matching_expiry,
        "valid_obs_count": valid_obs_count,
        "has_opt_def": has_opt_def_data
    }
        
    return event_id, fut_res, opt_res, metrics

def main():
    api_key = os.getenv('DATABENTO_API_KEY')
    if not api_key:
        print("DATABENTO_API_KEY missing. STOPPING Stage 1 Acquisition.")
        sys.exit(1)

    print("API Key found. Authenticated.")
    events_df = pd.read_csv('reports/RC015_Study_007_Acquisition_Summary.csv')
    qualifying = events_df[events_df['availability_status'] == 'QUALIFIED'].copy()

    fut_manifest = []
    opt_manifest = []

    print(f"Starting parallel processing of {len(qualifying)} events...")
    
    # Aggregators
    events_processed = 0
    events_with_valid_fut = 0
    events_no_fut_coverage = 0
    events_with_valid_opt_def = 0
    events_no_matching_expiry = 0
    events_no_eligible_options = 0
    
    total_calls = 0
    total_puts = 0
    api_symbology_errors = 0
    missing_market_data = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_event, idx, row, api_key): row for idx, row in qualifying.iterrows()}
        for future in concurrent.futures.as_completed(futures):
            event_id, f_res, o_res, metrics = future.result()
            events_processed += 1
            
            if metrics["symbology_err"]:
                api_symbology_errors += 1
            if metrics["missing_data"] > 0:
                missing_market_data += 1
                
            if metrics["bbo_missing"]:
                events_no_fut_coverage += 1
            else:
                events_with_valid_fut += 1
                
            if metrics["has_opt_def"]:
                events_with_valid_opt_def += 1
                
            if metrics["no_expiry"]:
                events_no_matching_expiry += 1
                
            if f_res:
                fut_manifest.append(f_res)
            
            if o_res is not None:
                if len(o_res) == 0:
                    events_no_eligible_options += 1
                else:
                    opt_manifest.extend(o_res)
                    for opt in o_res:
                        if opt['option_type'] == 'C': total_calls += 1
                        if opt['option_type'] == 'P': total_puts += 1
                        
            print(f"[{events_processed}/{len(qualifying)}] Event {event_id} processed.")

    fut_df = pd.DataFrame(fut_manifest)
    opt_df = pd.DataFrame(opt_manifest)

    # Save exactly as requested
    fut_df.to_csv('reports/RC015_Study_007_Futures_Instrument_Manifest.csv', index=False)
    opt_df.to_csv('reports/RC015_Study_007_Exact_Option_Instrument_Manifest.csv', index=False)

    num_fut_inst = fut_df['futures_instrument_id'].nunique() if not fut_df.empty else 0
    num_opt_inst = opt_df['instrument_id'].nunique() if not opt_df.empty else 0
    
    unique_parents = opt_df['option_parent'].unique().tolist() if not opt_df.empty else []
    
    # Calculate costs
    estimated_size_mb = num_opt_inst * 0.05 # ~50KB per option for a single day BBO-1m
    estimated_cost = (estimated_size_mb / 1000) * 17.00 # Assuming roughly $17/GB for Databento historical
    if estimated_cost < 0.01 and estimated_cost > 0: estimated_cost = 0.01

    with open('reports/RC015_Study_007_Stage1_Acquisition_Report.md', 'w', encoding='utf-8') as f:
        f.write("# RC015 Study 007 - Stage 1 Acquisition Report\n\n")
        
        f.write("## 1. Event Coverage Statistics\n")
        f.write(f"- **Events processed**: {events_processed}\n")
        f.write(f"- **Events with valid futures quotes**: {events_with_valid_fut}\n")
        f.write(f"- **Events with no futures coverage**: {events_no_fut_coverage}\n")
        f.write(f"- **Events with valid option definitions**: {events_with_valid_opt_def}\n")
        f.write(f"- **Events with no matching option expiry**: {events_no_matching_expiry}\n")
        f.write(f"- **Events with no eligible near-ATM options**: {events_no_eligible_options}\n\n")

        f.write("## 2. Discovered Instruments\n")
        f.write(f"- **Number of unique futures instruments**: {num_fut_inst}\n")
        f.write(f"- **Number of exact eligible option instruments**: {num_opt_inst}\n")
        f.write(f"- **Unique Option Parents used**: {', '.join(unique_parents) if unique_parents else 'None'}\n")
        f.write(f"- **Eligible Calls**: {total_calls}\n")
        f.write(f"- **Eligible Puts**: {total_puts}\n")
        f.write(f"- **MLEG/Spreads excluded**: Confirmed by security_type=OOF filtering.\n\n")
        
        f.write("## 3. Diagnostics\n")
        f.write(f"- **API/Symbology errors**: {api_symbology_errors}\n")
        f.write(f"- **Missing Market Data (Definitions)**: {missing_market_data}\n\n")
        
        f.write("## 4. Stage-2 Acquisition Projections\n")
        f.write(f"- **Proposed Stage-2 Option BBO requests (unique instruments)**: {num_opt_inst}\n")
        f.write(f"- **Estimated Stage-2 data volume**: ~{estimated_size_mb:.2f} MB\n")
        f.write(f"- **Estimated Stage-2 cost**: ${estimated_cost:.2f}\n")

if __name__ == '__main__':
    main()
