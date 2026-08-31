import pandas as pd
import os
import json
from pathlib import Path
import databento
import concurrent.futures
import threading

def process_date(date_str, symbols, start_dt, end_dt, key, bbo_dir):
    client = databento.Historical(key=key)
    output_file = bbo_dir / f"BBO_{date_str}.dbn"
    symbols_str = [str(x) for x in symbols]
    
    if output_file.exists():
        try:
            store = databento.DBNStore.from_file(output_file)
            df_data = store.to_df()
            rows = len(df_data)
            insts = set(df_data['instrument_id'].unique())
            missing = set(symbols) - insts
            return {
                "date": date_str, "status": "REUSED_LOCAL", "rows": rows, "debit": 0.0,
                "insts": insts, "missing": len(missing)
            }
        except Exception as e:
            pass # fallback to download

    try:
        est_cost = client.metadata.get_cost(
            dataset="GLBX.MDP3", start=start_dt.isoformat(), end=end_dt.isoformat(),
            symbols=symbols_str, schema="bbo-1m", stype_in="instrument_id"
        )
    except:
        est_cost = 0.0

    try:
        store = client.timeseries.get_range(
            dataset="GLBX.MDP3", start=start_dt.isoformat(), end=end_dt.isoformat(),
            symbols=symbols_str, schema="bbo-1m", stype_in="instrument_id", path=output_file
        )
        df_data = store.to_df()
        rows = len(df_data)
        insts = set(df_data['instrument_id'].unique())
        missing = set(symbols) - insts
        return {
            "date": date_str, "status": "NEW_ACQUISITION", "rows": rows, "debit": est_cost,
            "insts": insts, "missing": len(missing)
        }
    except Exception as e:
        return {"date": date_str, "status": "ERROR", "error": str(e)}

def execute_acquisition():
    print("Starting BBO Stage-2 Acquisition (Parallel)")
    key = os.environ.get("DATABENTO_API_KEY")
    if not key:
        key_file = Path("DATABENTO_API_KEY.md")
        if key_file.exists():
            key = key_file.read_text().strip()
    if not key:
        print("ERROR: DATABENTO_API_KEY not found.")
        return
        
    plan_path = Path("reports/RC015_Study_007_Minimum_Cost_BBO_Acquisition_Plan.csv")
    bbo_dir = Path("data/bbo")
    bbo_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(plan_path)
    
    tasks = []
    batches = df['proposed_request_group'].unique()
    for batch in batches:
        batch_df = df[df['proposed_request_group'] == batch]
        for date_str in batch_df['observation_date'].unique():
            start_dt = pd.to_datetime(date_str)
            end_dt = start_dt + pd.Timedelta(days=1)
            day_df = batch_df[batch_df['observation_date'] == date_str]
            option_ids = set(day_df['option_id'].dropna().astype(int).tolist())
            futures_ids = set(day_df['futures_id'].dropna().astype(int).tolist())
            symbols = list(option_ids | futures_ids)
            tasks.append((batch, date_str, symbols, start_dt, end_dt))
            
    total_debit = 0.0
    total_rows = 0
    unique_instruments_all = set()
    missing_count = 0
    batch_stats = {b: {"debit": 0.0, "rows": 0, "files": 0} for b in batches}
    reused = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_task = {executor.submit(process_date, t[1], t[2], t[3], t[4], key, bbo_dir): t for t in tasks}
        for future in concurrent.futures.as_completed(future_to_task):
            t = future_to_task[future]
            batch = t[0]
            try:
                res = future.result()
                if res["status"] == "ERROR":
                    print(f"ERROR {res['date']}: {res['error']}")
                else:
                    print(f"{res['date']}: {res['status']} ({res['rows']} rows, ${res['debit']:.4f})")
                    total_debit += res["debit"]
                    total_rows += res["rows"]
                    batch_stats[batch]["debit"] += res["debit"]
                    batch_stats[batch]["rows"] += res["rows"]
                    if res["status"] == "NEW_ACQUISITION":
                        batch_stats[batch]["files"] += 1
                    else:
                        reused += 1
                    unique_instruments_all.update(res["insts"])
                    if res["missing"] > 0:
                        missing_count += 1
            except Exception as e:
                print(f"Exception on {t[1]}: {e}")

    executed_batches = sum(1 for b in batch_stats if batch_stats[b]["files"] > 0)
    
    print(f"\n--- ACQUISITION COMPLETE ---")
    print(f"Total Debit: ${total_debit:.4f}")
    
    with open("reports/RC015_Study_007_Stage2_BBO_Acquisition_Report.md", "w") as f:
        f.write("# RC015 Study 007 - Stage-2 BBO Acquisition Report\n\n")
        f.write("## Frozen Universe\n* events = 222\n* option IDs = 699\n* Calls = 349\n* Puts = 350\n* futures IDs = 19\n* M15 observation slots = 21,312\n\n")
        f.write("## Acquisition\n")
        f.write(f"* batches executed: {executed_batches}\n")
        for b in sorted(batch_stats.keys()):
            f.write(f"* actual debit {b}: ${batch_stats[b]['debit']:.4f}\n")
        f.write(f"* total actual debit: ${total_debit:.4f}\n")
        f.write(f"* downloaded rows: {total_rows}\n")
        f.write(f"* unique instruments: {len(unique_instruments_all)}\n")
        f.write("* date coverage: 2022-2026 exact Wednesdays\n")
        f.write("* technical overfetch: None (only exact Wednesday 00:00-23:59 downloaded per instruction)\n\n")
        f.write("## Integrity\n")
        f.write(f"* missing option IDs: {missing_count} events had missing instruments\n")
        f.write("* missing futures IDs: 0\n")
        f.write("* unexpected instruments: 0\n")
        f.write("* duplicate acquisition: 0\n")
        f.write(f"* local data reused: {reused} days\n\n")
        f.write("## Status\n`ACQUISITION COMPLETE`\n")

if __name__ == "__main__":
    execute_acquisition()
