#!/usr/bin/env python3
"""
APEX IC6-R3 — Corrected BTC Options Eligibility Re-Validation

Fixes the IC6-R2 TTE computation bug (Python loop-variable scoping) and
applies IC6-R2-CR control-approved corrections:

  1. TTE computed from each row's own prediction timestamp (not batch residual)
  2. Maturity window: [12h, 24h] (nearest daily expiry only)
  3. Freshness: trade timestamp <= prediction timestamp AND age <= 1 hour
  4. IV source: pre-computed Black-76 from trade data (unchanged)
  5. Strike: nearest to index price from trade record (unchanged)

Uses the same Deribit History API v2 endpoint as IC6-R2.
Caches raw trade data to avoid re-fetching on re-runs.
"""

import asyncio
import httpx
import json
import time
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
import pandas as pd
import numpy as np

# ── Configuration ──────────────────────────────────────────────────────
BASE_URL = "https://history.deribit.com/api/v2/public"
MAX_RPS = 15
MAX_RETRIES = 3
RETRY_DELAY = 2.0
DATA_DIR = Path(__file__).parent.parent / "data" / "btc"
RAW_CACHE_FILE = DATA_DIR / "ic6r3_raw_trade_cache.json"
ELIGIBILITY_FILE = DATA_DIR / "ic6r3_results.json"
REPORTS_DIR = Path(__file__).parent.parent / "reports"


# ── API Fetch ──────────────────────────────────────────────────────────
async def fetch_trades(client, semaphore, start_ms, end_ms, retries=MAX_RETRIES):
    url = f"{BASE_URL}/get_last_trades_by_currency_and_time"
    params = {
        "currency": "BTC", "kind": "option", "count": 1000,
        "start_timestamp": start_ms, "end_timestamp": end_ms, "sorting": "desc",
    }
    for attempt in range(retries):
        try:
            async with semaphore:
                resp = await client.get(url, params=params, timeout=30)
                if resp.status_code == 200:
                    return resp.json().get("result", {}).get("trades", [])
                elif resp.status_code == 429:
                    await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    await asyncio.sleep(RETRY_DELAY)
        except Exception:
            await asyncio.sleep(RETRY_DELAY)
    return []


# ── Instrument Parsing ─────────────────────────────────────────────────
MONTH_MAP = {"JAN":1,"FEB":2,"MAR":3,"APR":4,"MAY":5,"JUN":6,
             "JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}

def parse_instrument(name):
    """Parse BTC-DDMMMYY-STRIKE-C/P -> dict with expiry_dt, strike, option_type."""
    try:
        parts = name.split("-")
        if len(parts) != 4: return None
        exp_str = parts[1]
        day = int(exp_str[:2])
        month = MONTH_MAP.get(exp_str[2:5], 0)
        year = 2000 + int(exp_str[5:])
        if month == 0: return None
        return {
            "expiry_dt": datetime(year, month, day, 8, 0, tzinfo=timezone.utc),
            "strike": float(parts[2]),
            "option_type": parts[3],
        }
    except Exception:
        return None


def compute_tte(expiry_dt, ref_dt):
    """TTE in hours from ref_dt to expiry_dt. Both must be tz-aware UTC."""
    if hasattr(ref_dt, 'to_pydatetime'):
        ref_dt = ref_dt.to_pydatetime()
    if hasattr(ref_dt, 'tzinfo') and ref_dt.tzinfo is None:
        ref_dt = ref_dt.replace(tzinfo=timezone.utc)
    return (expiry_dt - ref_dt).total_seconds() / 3600


# ── Eligibility Evaluation (per-timestamp, no scoping bugs) ───────────
def evaluate_timestamp(ts_str, episode_idx, trades, raw_trades_available=True):
    """
    Evaluate eligibility for a SINGLE prediction timestamp.

    Parameters
    ----------
    ts_str : str  — prediction timestamp as "YYYY-MM-DD HH:MM:SS"
    episode_idx : int
    trades : list — raw trade dicts from the API (all BTC option trades in [ts-24h, ts])

    Returns dict with eligibility fields.
    """
    ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

    base = {
        "timestamp": ts_str, "episode_idx": episode_idx,
        "n_trades": len(trades),
        "el_1_ic3_exists": True, "el_10_future_path": True,
    }

    if not trades:
        return {**base, "status": "NO_TRADES", "eligible": False,
                "el_2_option_data": False, "el_3_valid_underlying": False,
                "el_4_valid_strike": False, "el_5_call_exists": False,
                "el_6_put_exists": False, "el_7_maturity_ok": False,
                "el_8_freshness": False, "el_9_iv_valid": False,
                "atm_strike": None, "atm_iv": None, "atm_tte_hours": None,
                "atm_instrument": None, "trade_timestamp": None, "trade_age_h": None,
                "call_instrument": None, "put_instrument": None,
                "call_iv": None, "put_iv": None, "call_trade_ts": None, "put_trade_ts": None}

    # ── Step 1: Parse all trades and apply freshness filter ──
    parsed = []
    for t in trades:
        info = parse_instrument(t.get("instrument_name", ""))
        if info is None:
            continue
        trade_ts_ms = t.get("timestamp", 0)
        trade_dt = datetime.fromtimestamp(trade_ts_ms / 1000, tz=timezone.utc)

        # FRESHNESS: trade must be strictly before or at prediction timestamp
        if trade_dt > ts:
            continue  # reject future trades
        age_h = (ts - trade_dt).total_seconds() / 3600
        if age_h > 1.0:
            continue  # reject stale trades (> 1h old)

        iv_val = t.get("iv")
        if iv_val is None or iv_val <= 0:
            continue  # reject invalid IV

        parsed.append({
            "instrument": t["instrument_name"],
            "strike": info["strike"],
            "option_type": info["option_type"],
            "expiry_dt": info["expiry_dt"],
            "iv": iv_val,
            "trade_ts_ms": trade_ts_ms,
            "trade_dt": trade_dt,
            "trade_age_h": age_h,
            "index_price": t.get("index_price"),
        })

    base["el_2_option_data"] = len(trades) > 0

    if not parsed:
        return {**base, "status": "NO_FRESH_TRADES", "eligible": False,
                "el_3_valid_underlying": False, "el_4_valid_strike": False,
                "el_5_call_exists": False, "el_6_put_exists": False,
                "el_7_maturity_ok": False, "el_8_freshness": False,
                "el_9_iv_valid": False,
                "atm_strike": None, "atm_iv": None, "atm_tte_hours": None,
                "atm_instrument": None, "trade_timestamp": None, "trade_age_h": None,
                "call_instrument": None, "put_instrument": None,
                "call_iv": None, "put_iv": None, "call_trade_ts": None, "put_trade_ts": None}

    # ── Step 2: Index price from most recent trade ──
    parsed.sort(key=lambda x: x["trade_ts_ms"], reverse=True)
    index_price = parsed[0]["index_price"]
    if index_price is None or index_price <= 0:
        return {**base, "status": "NO_INDEX", "eligible": False,
                "el_3_valid_underlying": False, "el_4_valid_strike": False,
                "el_5_call_exists": False, "el_6_put_exists": False,
                "el_7_maturity_ok": False, "el_8_freshness": True,
                "el_9_iv_valid": False,
                "atm_strike": None, "atm_iv": None, "atm_tte_hours": None,
                "atm_instrument": None, "trade_timestamp": None, "trade_age_h": None,
                "call_instrument": None, "put_instrument": None,
                "call_iv": None, "put_iv": None, "call_trade_ts": None, "put_trade_ts": None}

    base["el_3_valid_underlying"] = True

    # ── Step 3: Nearest strike ──
    strikes = sorted(set(p["strike"] for p in parsed))
    atm_strike = min(strikes, key=lambda s: abs(s - index_price))
    atm_trades = [p for p in parsed if p["strike"] == atm_strike]
    base["el_4_valid_strike"] = True

    # ── Step 4: Compute TTE for THIS prediction timestamp ──
    # Group by (option_type, expiry_dt)
    groups = {}
    for t in atm_trades:
        key = (t["option_type"], t["expiry_dt"])
        groups.setdefault(key, []).append(t)

    # Find expiries in [12h, 24h]
    candidates_12_24 = []
    for (otype, expiry), grp in groups.items():
        tte = compute_tte(expiry, ts)  # <-- BUG FIX: use THIS ts, not batch residual
        if tte <= 0:
            continue
        if 12 <= tte <= 24:
            candidates_12_24.append((tte, otype, expiry, grp))

    if not candidates_12_24:
        # No expiry in [12h, 24h]
        return {**base, "status": "NO_MATURITY_MATCH", "eligible": False,
                "el_5_call_exists": False, "el_6_put_exists": False,
                "el_7_maturity_ok": False, "el_8_freshness": True, "el_9_iv_valid": False,
                "atm_strike": atm_strike, "atm_iv": None, "atm_tte_hours": None,
                "atm_instrument": None, "trade_timestamp": None, "trade_age_h": None,
                "call_instrument": None, "put_instrument": None,
                "call_iv": None, "put_iv": None, "call_trade_ts": None, "put_trade_ts": None}

    # ── Step 5: Select best expiry (closest to 18h = midpoint of [12,24]) ──
    candidates_12_24.sort(key=lambda x: abs(x[0] - 18))
    best_tte, best_otype, best_expiry, best_group = candidates_12_24[0]

    # ── Step 6: Find call and put at this strike/expiry ──
    # Collect ALL fresh trades at this strike+expiry across both C and P groups
    all_at_expiry = []
    for (otype, expiry), grp in groups.items():
        if expiry == best_expiry:
            all_at_expiry.extend(grp)
    call_grp = [(t["trade_dt"], t["iv"], t["instrument"], t["trade_age_h"])
                for t in all_at_expiry if t["option_type"] == "C"]
    put_grp  = [(t["trade_dt"], t["iv"], t["instrument"], t["trade_age_h"])
                for t in all_at_expiry if t["option_type"] == "P"]

    has_call = len(call_grp) > 0
    has_put  = len(put_grp) > 0

    base["el_5_call_exists"] = has_call
    base["el_6_put_exists"] = has_put

    if not (has_call and has_put):
        return {**base, "status": "MISSING_LEG", "eligible": False,
                "el_7_maturity_ok": True, "el_8_freshness": True, "el_9_iv_valid": False,
                "atm_strike": atm_strike, "atm_iv": None, "atm_tte_hours": round(best_tte, 2),
                "atm_instrument": None, "trade_timestamp": None, "trade_age_h": None,
                "call_instrument": call_grp[0][2] if call_grp else None,
                "put_instrument": put_grp[0][2] if put_grp else None,
                "call_iv": call_grp[0][1] if call_grp else None,
                "put_iv": put_grp[0][1] if put_grp else None,
                "call_trade_ts": call_grp[0][0].isoformat() if call_grp else None,
                "put_trade_ts": put_grp[0][0].isoformat() if put_grp else None}

    # Use most recent trade for each leg
    call_grp.sort(key=lambda x: x[0], reverse=True)
    put_grp.sort(key=lambda x: x[0], reverse=True)
    call_trade_dt, call_iv, call_instr, call_age = call_grp[0]
    put_trade_dt, put_iv, put_instr, put_age = put_grp[0]

    # Average IV for the straddle proxy (or use call if put is missing — already checked)
    avg_iv = (call_iv + put_iv) / 2

    # Use the freshest trade age
    trade_age = min(call_age, put_age)

    return {
        **base,
        "status": "ELIGIBLE",
        "eligible": True,
        "el_7_maturity_ok": True,
        "el_8_freshness": True,
        "el_9_iv_valid": True,
        "atm_strike": atm_strike,
        "atm_iv": round(avg_iv, 4),
        "atm_tte_hours": round(best_tte, 2),
        "atm_instrument": f"{call_instr}/{put_instr}",
        "trade_timestamp": call_trade_dt.isoformat(),
        "trade_age_h": round(trade_age, 4),
        "call_instrument": call_instr,
        "put_instrument": put_instr,
        "call_iv": round(call_iv, 4),
        "put_iv": round(put_iv, 4),
        "call_trade_ts": call_trade_dt.isoformat(),
        "put_trade_ts": put_trade_dt.isoformat(),
    }


# ── Main ───────────────────────────────────────────────────────────────
async def run_ic6r3():
    print("=" * 70)
    print("APEX IC6-R3 — Corrected BTC Options Eligibility Re-Validation")
    print("Fixes: TTE scoping bug, maturity [12h,24h], freshness <= 1h")
    print("=" * 70)

    # Load IC3 prediction timestamps
    ic3_path = Path(__file__).parent.parent / "reports" / "APEX_IC3_BTC_Transferability_Data.csv"
    ic3_df = pd.read_csv(ic3_path)
    ic3_df["ts"] = pd.to_datetime(ic3_df["onset_timestamp"])
    oos_df = ic3_df[ic3_df["ts"] >= "2023-01-01"].copy().reset_index(drop=True)

    print(f"\nIC3 OOS timestamps (>= 2023): {len(oos_df)}")
    print(f"Date range: {oos_df['ts'].min()} to {oos_df['ts'].max()}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Load raw trade cache (keyed by prediction timestamp string)
    raw_cache = {}
    if RAW_CACHE_FILE.exists():
        with open(RAW_CACHE_FILE) as f:
            raw_cache = json.load(f)
        print(f"Loaded raw trade cache: {len(raw_cache)} entries")

    semaphore = asyncio.Semaphore(MAX_RPS)
    api_calls = 0

    # Fetch raw trades for each timestamp
    print(f"\nFetching/retrieving trades for {len(oos_df)} timestamps...")
    async with httpx.AsyncClient() as client:
        for i, (_, row) in enumerate(oos_df.iterrows()):
            ts = row["ts"]
            ts_key = ts.strftime("%Y-%m-%d %H:%M:%S")

            if ts_key in raw_cache:
                continue  # already cached

            start_ms = int((ts - timedelta(hours=24)).timestamp() * 1000)
            end_ms   = int(ts.timestamp() * 1000)
            trades = await fetch_trades(client, semaphore, start_ms, end_ms)
            api_calls += 1
            raw_cache[ts_key] = trades

            if (i + 1) % 100 == 0:
                print(f"  [{i+1}/{len(oos_df)}] API calls: {api_calls}")
                with open(RAW_CACHE_FILE, "w") as f:
                    json.dump(raw_cache, f)

            # Rate-limit spacing
            if api_calls % 50 == 0:
                await asyncio.sleep(0.5)

    # Save raw cache
    with open(RAW_CACHE_FILE, "w") as f:
        json.dump(raw_cache, f)
    print(f"Raw trade cache saved: {len(raw_cache)} entries, {api_calls} API calls this run")

    # ── Evaluate eligibility ────────────────────────────────────────────
    print("\nEvaluating eligibility with corrected logic...")
    results = []
    for _, row in oos_df.iterrows():
        ts_key = row["ts"].strftime("%Y-%m-%d %H:%M:%S")
        trades = raw_cache.get(ts_key, [])
        result = evaluate_timestamp(ts_key, row["episode_idx"], trades)
        results.append(result)

    # ── Attrition Table ─────────────────────────────────────────────────
    total = len(results)
    n_option_data = sum(1 for r in results if r.get("el_2_option_data"))
    n_fresh       = sum(1 for r in results if r.get("n_trades", 0) > 0 and
                        any(parse_instrument(t.get("instrument_name","")) is not None
                            for t in json.loads('[]')))  # approximate
    n_underlying  = sum(1 for r in results if r.get("el_3_valid_underlying"))
    n_strike      = sum(1 for r in results if r.get("el_4_valid_strike"))
    n_call        = sum(1 for r in results if r.get("el_5_call_exists"))
    n_put         = sum(1 for r in results if r.get("el_6_put_exists"))
    n_maturity    = sum(1 for r in results if r.get("el_7_maturity_ok"))
    n_fresh_ok    = sum(1 for r in results if r.get("el_8_freshness"))
    n_iv          = sum(1 for r in results if r.get("el_9_iv_valid"))
    n_eligible    = sum(1 for r in results if r.get("eligible"))

    print("\n" + "=" * 70)
    print("IC6-R3 RESULTS")
    print("=" * 70)
    print(f"\nTotal prediction timestamps:      {total}")
    print(f"Option data present:              {n_option_data}")
    print(f"Underlying/index price available: {n_underlying}")
    print(f"Nearest strike available:         {n_strike}")
    print(f"Call exists (fresh, correct TTE): {n_call}")
    print(f"Put exists (fresh, correct TTE):  {n_put}")
    print(f"Joint call+put:                   {sum(1 for r in results if r.get('el_5_call_exists') and r.get('el_6_put_exists'))}")
    print(f"Maturity [12h,24h]:               {n_maturity}")
    print(f"Freshness <= 1h:                  {n_fresh_ok}")
    print(f"IV valid:                         {n_iv}")
    print(f"\nFinal eligible observations:      {n_eligible}/{total} ({100*n_eligible/total:.1f}%)")

    if n_eligible >= 100:
        print(f"\n>>> IC6-R3 GATE: PASS — {n_eligible} >= 100 minimum")
    else:
        print(f"\n>>> IC6-R3 GATE: FAIL — {n_eligible} < 100 minimum")
        print(f">>> IC7 BLOCKED — INSUFFICIENT ELIGIBLE OBSERVATIONS")

    # ── IV stats ────────────────────────────────────────────────────────
    elig_ivs = [r["atm_iv"] for r in results if r.get("eligible") and r.get("atm_iv")]
    if elig_ivs:
        print(f"\nIV statistics (eligible):")
        print(f"  Count: {len(elig_ivs)}")
        print(f"  Mean:  {np.mean(elig_ivs):.2f}")
        print(f"  Median: {np.median(elig_ivs):.2f}")
        print(f"  Min:   {np.min(elig_ivs):.2f}")
        print(f"  Max:   {np.max(elig_ivs):.2f}")
        print(f"  Std:   {np.std(elig_ivs):.2f}")

    # ── TTE validation ─────────────────────────────────────────────────
    elig_ttes = [r["atm_tte_hours"] for r in results if r.get("eligible") and r.get("atm_tte_hours")]
    if elig_ttes:
        print(f"\nTTE statistics (eligible):")
        print(f"  Mean:  {np.mean(elig_ttes):.2f}h")
        print(f"  Min:   {np.min(elig_ttes):.2f}h")
        print(f"  Max:   {np.max(elig_ttes):.2f}h")

    # ── Trade age stats ─────────────────────────────────────────────────
    elig_ages = [r["trade_age_h"] for r in results if r.get("eligible") and r.get("trade_age_h") is not None]
    if elig_ages:
        ages = np.array(elig_ages)
        print(f"\nTrade age statistics (eligible):")
        print(f"  Mean:   {np.mean(ages)*60:.1f} min")
        print(f"  Median: {np.median(ages)*60:.1f} min")
        print(f"  Min:    {np.min(ages)*60:.1f} min")
        print(f"  Max:    {np.max(ages)*60:.1f} min")
        print(f"  <= 15m: {(ages <= 0.25).sum()}")
        print(f"  15-30m: {((ages > 0.25) & (ages <= 0.5)).sum()}")
        print(f"  30-60m: {((ages > 0.5) & (ages <= 1.0)).sum()}")

    # ── Save outputs ────────────────────────────────────────────────────
    res_df = pd.DataFrame(results)
    csv_path = REPORTS_DIR / "APEX_IC6R3_BTC_Options_Eligibility.csv"
    res_df.to_csv(csv_path, index=False)
    print(f"\nSaved eligibility ledger: {csv_path}")

    summary = {
        "total_timestamps": total,
        "api_calls_this_run": api_calls,
        "raw_cache_entries": len(raw_cache),
        "eligible": n_eligible,
        "minimum_required": 100,
        "gate_pass": n_eligible >= 100,
        "iv_mean": round(float(np.mean(elig_ivs)), 2) if elig_ivs else None,
        "iv_median": round(float(np.median(elig_ivs)), 2) if elig_ivs else None,
        "iv_min": round(float(np.min(elig_ivs)), 2) if elig_ivs else None,
        "iv_max": round(float(np.max(elig_ivs)), 2) if elig_ivs else None,
    }
    with open(ELIGIBILITY_FILE, "w") as f:
        json.dump(summary, f, indent=2)

    return results, summary


if __name__ == "__main__":
    results, summary = asyncio.run(run_ic6r3())
    print("\nDone.")
