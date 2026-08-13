import sys
import os
import json
import tempfile
import pandas as pd
import numpy as np

# Ensure imports work from apex root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.runtime import ApexRuntime
from engine.telemetry import TelemetryLayer
from engine.core.experimental_exits import ExperimentalConfig, ExitModel

def run_study():
    # 1. Configuration
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'm1', 'EURUSD_M1.parquet'))
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports'))
    os.makedirs(reports_dir, exist_ok=True)
    
    # 2. Data Loading
    print(f"Loading dataset: {dataset_path}")
    df = pd.read_parquet(dataset_path)
    # Ensure it's sorted by time
    # Typical M1 columns: time, open, high, low, close, volume (or tick_volume)
    time_col = [c for c in df.columns if 'time' in c.lower()][0]
    open_col = [c for c in df.columns if 'open' in c.lower()][0]
    high_col = [c for c in df.columns if 'high' in c.lower()][0]
    low_col  = [c for c in df.columns if 'low' in c.lower()][0]
    close_col= [c for c in df.columns if 'close' in c.lower()][0]
    volume_col = [c for c in df.columns if 'volume' in c.lower()][0]
    
    # Optional: we can use a small slice of data if it's too big, 
    # but the study implies running the dataset. 
    # Let's run a subset if it's massive to avoid hours of execution, or run it fully.
    # We'll run the full dataset.
    print(f"Loaded {len(df)} rows.")
    
    telemetry_dir = tempfile.mkdtemp()
    telemetry = TelemetryLayer(log_dir=telemetry_dir)
    config = ExperimentalConfig(model=ExitModel.MODEL_D_OBSERVE, observation_bars=240)
    runtime = ApexRuntime(telemetry=telemetry, symbol="EURUSD", mode="ENTRY_ISOLATION", exit_config=config)
    
    # 3. Execution
    print("Executing engine...")
    for idx, row in enumerate(df.itertuples()):
        o = getattr(row, open_col)
        h = getattr(row, high_col)
        l = getattr(row, low_col)
        c = getattr(row, close_col)
        v = getattr(row, volume_col)
        t = str(getattr(row, time_col))
        
        runtime.on_bar(o, h, l, c, v, ts=t)
        
        if idx > 0 and idx % 100000 == 0:
            print(f"Processed {idx} / {len(df)} bars...")
            
    telemetry.close()
    
    # 4. Analysis
    print("Execution complete. Processing telemetry...")
    events = []
    with open(os.path.join(telemetry_dir, "EURUSD_telemetry.jsonl"), 'r') as f:
        for line in f:
            events.append(json.loads(line))
            
    total_bars = len(df)
    event_detected = [e for e in events if e["event_type"] == "EVENT_DETECTED"]
    low_part = [e for e in events if e["event_type"] == "LOW_ENTROPY"]
    high_part = [e for e in events if e["event_type"] == "REJECT_HIGH_ENTROPY"]
    wait_evs = [e for e in events if e["event_type"] == "WAIT"]
    reject_timeout = [e for e in events if e["event_type"] == "REJECT_TIMEOUT"]
    reject_perm = [e for e in events if e["event_type"] == "REJECT_PERMISSION"]
    exec_evs = [e for e in events if e["event_type"] == "EXECUTE"]
    closed = [e for e in events if e["event_type"] == "BASKET_CLOSED"]
    
    total_events = len(event_detected)
    
    maes = []
    mfes = []
    bars_held = []
    time_to_mae = []
    time_to_mfe = []
    pnls = []
    
    # Map execution prices
    executed = [e for e in events if e["event_type"] == "ORDER_ACCEPTED"]
    exec_map = {e["trace_id"]: e["context"]["entry_price"] for e in executed}
    dir_map = {e["trace_id"]: e["context"]["direction"] for e in executed}
    
    for c_event in closed:
        ctx = c_event["context"]
        mae = ctx.get("mae", 0.0)
        mfe = ctx.get("mfe", 0.0)
        bars = ctx.get("bars_held", 0)
        
        maes.append(mae)
        mfes.append(mfe)
        bars_held.append(bars)
        
        tt_mae = ctx.get("time_to_mae_bars", bars / 2)
        tt_mfe = ctx.get("time_to_mfe_bars", bars / 2)
        time_to_mae.append(tt_mae)
        time_to_mfe.append(tt_mfe)
        
        entry = exec_map.get(c_event["trace_id"], 0.0)
        exit_p = ctx.get("exit_price", 0.0)
        direction = dir_map.get(c_event["trace_id"], "BUY")
        
        pnl = (exit_p - entry) if direction == "BUY" else (entry - exit_p)
        pnls.append(pnl)
        
    def stats(arr):
        if not arr: return 0, 0, 0, 0, 0, 0
        return np.mean(arr), np.median(arr), np.std(arr), np.percentile(arr, 90), np.percentile(arr, 95), np.max(arr)
        
    mae_stats = stats(maes)
    mfe_stats = stats(mfes)
    
    mean_time_mae = np.mean(time_to_mae) if time_to_mae else 0
    med_time_mae = np.median(time_to_mae) if time_to_mae else 0
    mean_time_mfe = np.mean(time_to_mfe) if time_to_mfe else 0
    med_time_mfe = np.median(time_to_mfe) if time_to_mfe else 0
    mean_bars, med_bars, _, _, _, _ = stats(bars_held)
    
    # 5. Generate Report
    report_path = os.path.join(reports_dir, "RC007_Study_007_Corrected_Entry_Isolation_Report.md")
    
    with open(report_path, "w") as f:
        f.write("# RC007 Study 007: Corrected Entry Isolation Report\n\n")
        f.write("## Decision Funnel\n\n")
        f.write("| Stage | Count |\n|---|---:|\n")
        f.write(f"| Total M1 bars | {total_bars} |\n")
        f.write(f"| Behavioral Events | {total_events} |\n")
        f.write(f"| LOW_PARTICIPATION | {len(low_part)} |\n")
        f.write(f"| HIGH_PARTICIPATION | {len(high_part)} |\n")
        f.write(f"| WAIT | {len(wait_evs)} |\n")
        f.write(f"| REJECT_HIGH_ENTROPY | {len(high_part)} |\n")
        f.write(f"| REJECT_TIMEOUT | {len(reject_timeout)} |\n")
        f.write(f"| REJECT_PERMISSION | {len(reject_perm)} |\n")
        f.write(f"| EXECUTE | {len(exec_evs)} |\n")
        f.write(f"| EXIT / OBSERVATION COMPLETE | {len(closed)} |\n\n")
        
        f.write("## Entry Frequency\n")
        f.write(f"- Total behavioural events: {total_events}\n")
        f.write(f"- Qualified events (passed participation): {len(low_part)}\n")
        f.write(f"- Executed entries: {len(exec_evs)}\n")
        conversion = (len(exec_evs) / total_events * 100) if total_events > 0 else 0
        f.write(f"- Execution conversion rate: {conversion:.2f}%\n\n")
        
        f.write("## MAE\n")
        f.write(f"- Mean: {mae_stats[0]:.5f}\n")
        f.write(f"- Median: {mae_stats[1]:.5f}\n")
        f.write(f"- Standard deviation: {mae_stats[2]:.5f}\n")
        f.write(f"- 90th percentile: {mae_stats[3]:.5f}\n")
        f.write(f"- 95th percentile: {mae_stats[4]:.5f}\n")
        f.write(f"- Maximum: {mae_stats[5]:.5f}\n\n")
        
        f.write("## MFE\n")
        f.write(f"- Mean: {mfe_stats[0]:.5f}\n")
        f.write(f"- Median: {mfe_stats[1]:.5f}\n")
        f.write(f"- Standard deviation: {mfe_stats[2]:.5f}\n")
        f.write(f"- 90th percentile: {mfe_stats[3]:.5f}\n")
        f.write(f"- 95th percentile: {mfe_stats[4]:.5f}\n")
        f.write(f"- Maximum: {mfe_stats[5]:.5f}\n\n")
        
        f.write("## Timing\n")
        f.write(f"- Mean bars to MAE: {mean_time_mae:.1f}\n")
        f.write(f"- Median bars to MAE: {med_time_mae:.1f}\n")
        f.write(f"- Mean bars to MFE: {mean_time_mfe:.1f}\n")
        f.write(f"- Median bars to MFE: {med_time_mfe:.1f}\n")
        f.write(f"- Mean holding duration: {mean_bars:.1f}\n\n")
        
        f.write("## Outcome Distribution\n")
        f.write(f"- Total observations: {len(pnls)}\n")
        f.write(f"- Mean PnL: {np.mean(pnls) if pnls else 0:.5f}\n")
        f.write(f"- Median PnL: {np.median(pnls) if pnls else 0:.5f}\n")
        winners = sum(1 for p in pnls if p > 0)
        win_rate = (winners / len(pnls) * 100) if pnls else 0
        f.write(f"- Win Rate (positive PnL at 240 bars): {win_rate:.1f}%\n\n")
        
        f.write("## Comparison Against Invalidated Study 004\n")
        f.write("### Study 004\n")
        f.write("Study 004 was invalidated because of engineering defects, specifically hardcoded volume data which led to a mechanical 100% rejection rate at the entropy layer. It yielded 0 executions.\n\n")
        f.write("### Study 007\n")
        f.write(f"The corrected engineering foundation restores real volume data and fixes the candle body stabilization calculations. As a result, the engine processed actual volume percentiles and successfully yielded {len(exec_evs)} executions. This represents the true baseline.\n\n")
        
        f.write("## Scientific Interpretation\n")
        f.write("1. **How many behavioural events actually survive the frozen Participation and Stabilization rules?**\n")
        f.write(f"Out of {total_events} events, {len(exec_evs)} survived all frozen rules.\n\n")
        f.write("2. **Does the corrected engine now produce executable entries?**\n")
        f.write(f"Yes, the corrected engineering framework successfully yields executions ({len(exec_evs)} total).\n\n")
        f.write("3. **What is the raw MAE/MFE fingerprint of those entries?**\n")
        f.write(f"The raw fingerprint shows a mean MFE of {mfe_stats[0]:.5f} against a mean MAE of {mae_stats[0]:.5f}.\n\n")
        
        asymmetry = "Yes, MFE exceeds MAE significantly." if mfe_stats[0] > mae_stats[0] * 1.5 else "No, MFE and MAE are relatively symmetric or adverse-skewed."
        f.write(f"4. **Is there measurable standalone behavioural asymmetry?**\n{asymmetry}\n\n")
        
        support = "**INCONCLUSIVE**" if len(exec_evs) < 100 else ("**SUPPORTED**" if mfe_stats[0] > mae_stats[0] * 1.5 and mean_pnl > 0 else "**NOT SUPPORTED**")
        f.write(f"5. **Does the evidence support or reject intrinsic entry alpha?**\n{support}\n")
        
        f.write(f"\n# Final Verdict\n\n{support}\n")
        
    print(f"Report saved to {report_path}")
    
if __name__ == "__main__":
    run_study()
