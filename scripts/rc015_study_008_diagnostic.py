import pandas as pd
import numpy as np
from pathlib import Path
import databento
import time

def evaluate_design(design_name, target_times_utc):
    print(f"\nEvaluating Design: {design_name}", flush=True)
    manifest_path = Path("reports/RC015_Study_007_Final_Moneyness_Revalidation.csv")
    df_man = pd.read_csv(manifest_path)
    df_man = df_man[df_man["moneyness_status"] == "PASS"]
    
    bbo_dir = Path("data/bbo")
    rec_dir = Path("data/databento/rc015_stage2_recovery")
    
    date_to_files = {}
    for f in list(bbo_dir.glob("*.dbn")) + list(rec_dir.glob("*.dbn")):
        dt = f.stem.split("_")[-1]
        if dt not in date_to_files:
            date_to_files[dt] = []
        date_to_files[dt].append(f)
        
    out_rows = []
    events_by_date = df_man.groupby("observation_date")
    
    for obs_date, ev_group in events_by_date:
        targets = []
        for _, man_row in ev_group.iterrows():
            ev_id = man_row["event_id"]
            opt_id = man_row["option_instrument_id"]
            fut_id = man_row["futures_instrument_id"]
            for t_str in target_times_utc:
                ts_t = pd.to_datetime(f"{obs_date}T{t_str}", utc=True)
                targets.append({
                    "event_id": ev_id,
                    "ts_t": ts_t,
                    "option_id": opt_id,
                    "futures_id": fut_id
                })
                
        df_targets = pd.DataFrame(targets).sort_values("ts_t")
        df_targets["ts_t"] = df_targets["ts_t"].astype("datetime64[ns, UTC]")
        df_targets["option_id"] = df_targets["option_id"].astype("uint32")
        df_targets["futures_id"] = df_targets["futures_id"].astype("uint32")
        
        files = date_to_files.get(obs_date, [])
        dfs = []
        for f in files:
            try:
                store = databento.DBNStore.from_file(f)
                df_part = store.to_df()
                if len(df_part) > 0:
                    dfs.append(df_part)
            except:
                pass
                
        if dfs:
            df_day = pd.concat(dfs).sort_values("ts_event")
        else:
            df_day = pd.DataFrame(columns=["instrument_id", "ts_event"])
            
        if not df_day.empty and df_day["ts_event"].dt.tz is None:
            df_day["ts_event"] = df_day["ts_event"].dt.tz_localize("UTC")
            
        if not df_day.empty:
            df_day["instrument_id"] = df_day["instrument_id"].astype("uint32")
            df_day["ts_event"] = pd.to_datetime(df_day["ts_event"], utc=True).astype("datetime64[ns, UTC]")
            df_day = df_day.dropna(subset=["ts_event", "instrument_id"])
            df_targets = df_targets.dropna(subset=["ts_t", "option_id", "futures_id"])
            
        df_opt_state = pd.merge_asof(
            df_targets,
            df_day[["instrument_id", "ts_event"]],
            left_on="ts_t",
            right_on="ts_event",
            left_by="option_id",
            right_by="instrument_id",
            direction="backward"
        ).rename(columns={"ts_event": "opt_ts"})
        
        df_fut_state = pd.merge_asof(
            df_targets,
            df_day[["instrument_id", "ts_event"]],
            left_on="ts_t",
            right_on="ts_event",
            left_by="futures_id",
            right_by="instrument_id",
            direction="backward"
        ).rename(columns={"ts_event": "fut_ts"})
        
        for i in range(len(df_targets)):
            row = df_opt_state.iloc[i]
            opt_ts = row["opt_ts"]
            fut_ts = df_fut_state.iloc[i]["fut_ts"]
            ts_t = row["ts_t"]
            
            opt_age_sec = (ts_t - opt_ts).total_seconds() if pd.notnull(opt_ts) else np.nan
            fut_age_sec = (ts_t - fut_ts).total_seconds() if pd.notnull(fut_ts) else np.nan
            
            out_rows.append({
                "event_id": row["event_id"],
                "opt_age_sec": opt_age_sec,
                "fut_age_sec": fut_age_sec
            })

    df = pd.DataFrame(out_rows)
    
    # Calculate coverage diagnostics
    total_slots = len(df)
    
    # Events with at least one valid option quote (age not null)
    df_valid = df[df["opt_age_sec"].notnull()]
    events_covered = df_valid["event_id"].nunique()
    pct_events_covered = events_covered / 222.0
    
    # For sync slots we require both option and future to have the same age requirement
    sync_5m = len(df[(df["opt_age_sec"] <= 300) & (df["fut_age_sec"] <= 300)])
    sync_15m = len(df[(df["opt_age_sec"] <= 900) & (df["fut_age_sec"] <= 900)])
    sync_30m = len(df[(df["opt_age_sec"] <= 1800) & (df["fut_age_sec"] <= 1800)])
    sync_60m = len(df[(df["opt_age_sec"] <= 3600) & (df["fut_age_sec"] <= 3600)])
    
    pct_5m = sync_5m / total_slots if total_slots > 0 else 0
    pct_15m = sync_15m / total_slots if total_slots > 0 else 0
    pct_30m = sync_30m / total_slots if total_slots > 0 else 0
    pct_60m = sync_60m / total_slots if total_slots > 0 else 0
    
    if len(df_valid) > 0:
        med_age = df_valid["opt_age_sec"].median()
        p90_age = df_valid["opt_age_sec"].quantile(0.9)
    else:
        med_age = np.nan
        p90_age = np.nan
        
    print(f"Events Covered: {events_covered}/222 ({pct_events_covered:.1%})")
    print(f"<=5m: {sync_5m} ({pct_5m:.1%})")
    print(f"<=15m: {sync_15m} ({pct_15m:.1%})")
    print(f"<=30m: {sync_30m} ({pct_30m:.1%})")
    print(f"<=60m: {sync_60m} ({pct_60m:.1%})")
    print(f"Median Age: {med_age}s")
    print(f"P90 Age: {p90_age}s")
    
    return {
        "Design": design_name,
        "Events Covered": events_covered,
        "<=5m": pct_5m,
        "<=15m": pct_15m,
        "<=30m": pct_30m,
        "<=60m": pct_60m,
        "Median Age": med_age,
        "P90 Age": p90_age
    }

if __name__ == "__main__":
    designs = [
        ("Design A - Fixed Daily Anchor", ["14:00:00Z"]),
        ("Design B - Fixed Two-Anchor", ["08:00:00Z", "14:00:00Z"]),
        ("Design C - Liquid Window", [f"{h:02d}:{m:02d}:00Z" for h in range(12, 17) for m in (0, 15, 30, 45) if not (h==16 and m>0)]),
        ("Design D - Transition Anchors", ["06:00:00Z", "08:00:00Z", "12:00:00Z", "16:00:00Z"])
    ]
    
    results = []
    for name, times in designs:
        res = evaluate_design(name, times)
        results.append(res)
        
    df_res = pd.DataFrame(results)
    df_res.to_csv("reports/RC015_Study_008_temp_results.csv", index=False)
    print("\nDONE!")
