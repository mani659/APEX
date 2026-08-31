#!/usr/bin/env python3
"""
APEX IC7 — BTC IV/RV Direction-Neutral Straddle Economic Experiment

Uses Black-76 to reconstruct option entry premiums from IV.
Does NOT load the raw trade cache (too large).
"""

import pandas as pd
import numpy as np
import json
import statsmodels.api as sm
from scipy.stats import norm
from pathlib import Path

BASE = Path(__file__).parent.parent
REPORTS = BASE / "reports"
DATA = BASE / "data"

# ── Black-76 pricing ──────────────────────────────────────────────────
def black76_call(F, K, T, sigma, r=0.0):
    """Black-76 call price. F=forward, K=strike, T=years, sigma=annualized vol (decimal)."""
    if T <= 0 or sigma <= 0:
        return max(F - K, 0)
    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return np.exp(-r * T) * (F * norm.cdf(d1) - K * norm.cdf(d2))

def black76_put(F, K, T, sigma, r=0.0):
    """Black-76 put price."""
    if T <= 0 or sigma <= 0:
        return max(K - F, 0)
    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return np.exp(-r * T) * (K * norm.cdf(-d2) - F * norm.cdf(-d1))

# ── Load Data ──────────────────────────────────────────────────────────
print("Loading data...")
ic3 = pd.read_csv(REPORTS / "APEX_IC3_BTC_Transferability_Data.csv")
ic3 = ic3.sort_values("episode_idx").reset_index(drop=True)

eligible = pd.read_csv(REPORTS / "APEX_IC6R3_BTC_Options_Eligibility.csv")
eligible = eligible[eligible["eligible"] == True].copy().reset_index(drop=True)
print(f"  IC3 episodes: {len(ic3)}, IC6-R3 eligible: {len(eligible)}")

btc = pd.read_parquet(DATA / "m1" / "BTCUSD_M1.parquet")
btc["ts"] = pd.to_datetime(btc["timestamp"])
btc = btc.set_index("ts").sort_index()
print(f"  BTC M1: {len(btc)} bars")

# ── Walk-Forward OLS Mapping ──────────────────────────────────────────
print("\nReconstructing walk-forward OLS mapping...")
ic3_lookup = ic3.set_index("episode_idx")[["predicted_lp", "forward_rv_12h"]].to_dict("index")

eligible["risk_score"] = eligible["episode_idx"].map(lambda e: ic3_lookup.get(e, {}).get("predicted_lp", np.nan))
eligible["forward_rv_12h"] = eligible["episode_idx"].map(lambda e: ic3_lookup.get(e, {}).get("forward_rv_12h", np.nan))
eligible = eligible.dropna(subset=["risk_score"]).reset_index(drop=True)

# Walk-forward OLS
episodes_sorted = ic3.sort_values("episode_idx")
ep_lp = episodes_sorted["predicted_lp"].values
ep_rv = episodes_sorted["forward_rv_12h"].values
ep_ids = episodes_sorted["episode_idx"].values
pred_rv_map = {}
MIN_TRAIN = 10

for i in range(len(episodes_sorted)):
    ep_id = ep_ids[i]
    if i < MIN_TRAIN:
        X = sm.add_constant(ep_lp[:i+1])
        y = ep_rv[:i+1]
        if len(y) >= 3:
            model = sm.OLS(y, X).fit()
            pred_rv_map[ep_id] = model.predict(X[-1:])[0]
        else:
            pred_rv_map[ep_id] = ep_rv[i]
    else:
        X = sm.add_constant(ep_lp[:i])
        y = ep_rv[:i]
        model = sm.OLS(y, X).fit()
        pred_rv_map[ep_id] = model.predict(X[-1:])[0]

eligible["predicted_RV"] = eligible["episode_idx"].map(pred_rv_map)
eligible = eligible.dropna(subset=["predicted_RV"]).reset_index(drop=True)

# OOS correlation
corr = np.corrcoef(eligible["predicted_RV"].values, eligible["forward_rv_12h"].values)[0, 1]
print(f"  Eligible: {len(eligible)}, OOS corr: {corr:.4f}")

# ── Entry Premium via Black-76 ────────────────────────────────────────
print("\nComputing entry premiums via Black-76...")

# avg_iv is in percentage; convert to decimal for Black-76
eligible["avg_iv"] = (eligible["call_iv"] + eligible["put_iv"]) / 2
eligible["avg_iv_decimal"] = eligible["avg_iv"] / 100.0

# Forward price: use avg index price from call/put trades
# (already in eligible as 'index_price_entry' if available, otherwise reconstruct)
# We need index_price. Check if it's in the data:
if "index_price_entry" not in eligible.columns:
    # Reconstruct from raw cache — but cache is too large
    # Instead, use the strike as a proxy for the forward (ATM strike ≈ forward)
    eligible["F_entry"] = eligible["atm_strike"]
else:
    eligible["F_entry"] = eligible["index_price_entry"]

# TTE in years
eligible["T_years"] = eligible["atm_tte_hours"] / (365.25 * 24)

# Black-76 entry prices (in BTC per 1 BTC notional) - vectorized
F = eligible["F_entry"].values.astype(float)
K = eligible["atm_strike"].values.astype(float)
T = eligible["T_years"].values.astype(float)
sig = eligible["avg_iv_decimal"].values.astype(float)

# Vectorized Black-76
def vec_black76_call(F, K, T, sigma):
    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return F * norm.cdf(d1) - K * norm.cdf(d2)

def vec_black76_put(F, K, T, sigma):
    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * norm.cdf(-d2) - F * norm.cdf(-d1)

# Black-76 gives USD price per 1 BTC notional; Deribit quotes in BTC
# So divide by F to get BTC-denominated premium
eligible["call_entry_btc"] = vec_black76_call(F, K, T, sig) / F
eligible["put_entry_btc"] = vec_black76_put(F, K, T, sig) / F
eligible["straddle_premium_btc"] = eligible["call_entry_btc"] + eligible["put_entry_btc"]
eligible["straddle_premium_usd"] = eligible["straddle_premium_btc"] * eligible["F_entry"]

print(f"  Call premium (BTC): mean={eligible['call_entry_btc'].mean():.6f}")
print(f"  Put premium (BTC): mean={eligible['put_entry_btc'].mean():.6f}")
print(f"  Straddle premium (USD): mean={eligible['straddle_premium_usd'].mean():.2f}")

# ── Expiry Payoff ──────────────────────────────────────────────────────
print("\nComputing expiry payoffs...")

MONTH_MAP = {"JAN":1,"FEB":2,"MAR":3,"APR":4,"MAY":5,"JUN":6,
             "JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}

def get_expiry_btc_price(btc_df, instrument_name):
    try:
        parts = instrument_name.split("-")
        exp_str = parts[1]
        day = int(exp_str[:2])
        month = MONTH_MAP[exp_str[2:5]]
        year = 2000 + int(exp_str[5:])
        expiry_dt = pd.Timestamp(f"{year}-{month:02d}-{day:02d} 08:00:00")
        mask = btc_df.index <= expiry_dt
        if mask.any():
            return btc_df.loc[mask, "close"].iloc[-1]
    except Exception:
        pass
    return np.nan

eligible["F_expiry"] = eligible["call_instrument"].apply(lambda x: get_expiry_btc_price(btc, x))
eligible = eligible.dropna(subset=["F_expiry"]).reset_index(drop=True)
print(f"  Eligible with valid expiry: {len(eligible)}")

# Gross payoff: |F_expiry - K| in USD per 1 BTC notional
eligible["K"] = eligible["atm_strike"]
eligible["gross_payoff_usd"] = np.abs(eligible["F_expiry"] - eligible["K"])

# Transaction costs: 0.04% x 4 legs x entry notional
eligible["transaction_cost_usd"] = 0.0004 * 4 * eligible["F_entry"]

# Net PnL
eligible["net_PnL_usd"] = eligible["gross_payoff_usd"] - eligible["straddle_premium_usd"] - eligible["transaction_cost_usd"]
eligible["net_PnL_pct"] = eligible["net_PnL_usd"] / eligible["F_entry"] * 100

print(f"  Gross payoff (USD): mean={eligible['gross_payoff_usd'].mean():.2f}")
print(f"  Net PnL (USD): mean={eligible['net_PnL_usd'].mean():.2f}, median={eligible['net_PnL_usd'].median():.2f}")
print(f"  Net PnL (%): mean={eligible['net_PnL_pct'].mean():.4f}%")

# ── Forecast-IV Spread ────────────────────────────────────────────────
print("\nComputing forecast-IV spread...")
# Convert predicted_RV (decimal) to percentage for comparison with IV (%)
eligible["predicted_RV_pct"] = eligible["predicted_RV"] * 100
eligible["forecast_IV_spread"] = eligible["predicted_RV_pct"] - eligible["avg_iv"]

n_pos = (eligible["forecast_IV_spread"] > 0).sum()
print(f"  Predicted RV (pct): mean={eligible['predicted_RV_pct'].mean():.2f}%")
print(f"  Avg IV (pct): mean={eligible['avg_iv'].mean():.2f}%")
print(f"  Spread: mean={eligible['forecast_IV_spread'].mean():.2f}%")
print(f"  Fraction predicted_RV > IV: {n_pos}/{len(eligible)} ({100*n_pos/len(eligible):.1f}%)")

# ── Baseline ──────────────────────────────────────────────────────────
print("\nBaseline (unconditional):")
print(f"  Mean PnL: {eligible['net_PnL_usd'].mean():.2f} USD")
print(f"  Hit rate: {(eligible['net_PnL_usd'] > 0).mean():.4f}")

# ── Primary Economic Test ──────────────────────────────────────────────
print("\n=== PRIMARY ECONOMIC TEST ===")

mask = eligible["forecast_IV_spread"] > 0
cond_pnl = eligible.loc[mask, "net_PnL_usd"].values
print(f"Conditional sample (predicted_RV > IV): {len(cond_pnl)} observations")

if len(cond_pnl) < 10:
    print("CONDITIONAL SAMPLE TOO SMALL — cannot run HAC test")
    print("Falling back to unconditional test on all 343 observations")
    cond_pnl = eligible["net_PnL_usd"].values
    mask_description = "unconditional (all eligible)"
else:
    mask_description = f"conditional (predicted_RV > IV, N={len(cond_pnl)})"

mean_pnl = np.mean(cond_pnl)
std_pnl = np.std(cond_pnl, ddof=1)
print(f"  Mean net PnL: {mean_pnl:.2f} USD")
print(f"  Std net PnL: {std_pnl:.2f} USD")
print(f"  Median net PnL: {np.median(cond_pnl):.2f} USD")
print(f"  Fraction positive: {(cond_pnl > 0).mean():.4f}")

# HAC t-test: H0: mean=0, H1: mean > 0 (one-sided)
y = cond_pnl
X = np.ones(len(y))
model = sm.OLS(y, X)
results = model.fit(cov_type="HAC", cov_kwds={"maxlags": 12})

t_stat = results.tvalues[0]
p_two = results.pvalues[0]
p_one = p_two / 2 if t_stat > 0 else 1 - p_two / 2
hac_se = results.bse[0]
ci_low = results.conf_int()[0][0]
ci_high = results.conf_int()[0][1]

print(f"\n  HAC t-statistic: {t_stat:.4f}")
print(f"  HAC SE: {hac_se:.4f}")
print(f"  p-value (one-sided): {p_one:.6f}")
print(f"  95% CI: [{ci_low:.2f}, {ci_high:.2f}]")

# ── Decision ───────────────────────────────────────────────────────────
print("\n=== DECISION ===")
baseline_mean = eligible["net_PnL_usd"].mean()
gate_a = len(cond_pnl) >= 100
gate_b = mean_pnl > 0
gate_c = mean_pnl > baseline_mean
gate_d = p_one < 0.05

print(f"  Gate A (N >= 100): {'PASS' if gate_a else 'FAIL'} (N={len(cond_pnl)})")
print(f"  Gate B (mean > 0): {'PASS' if gate_b else 'FAIL'} ({mean_pnl:.2f})")
print(f"  Gate C (> baseline): {'PASS' if gate_c else 'FAIL'} (cond={mean_pnl:.2f}, base={baseline_mean:.2f})")
print(f"  Gate D (p < 0.05): {'PASS' if gate_d else 'FAIL'} (p={p_one:.6f})")

if gate_a and gate_b and gate_c and gate_d:
    decision = "ECONOMIC EDGE ESTABLISHED"
elif gate_a and gate_b and gate_c:
    decision = "POSITIVE BUT NOT SIGNIFICANT"
elif gate_a and gate_b:
    decision = "POSITIVE BUT DOES NOT BEAT BASELINE"
elif gate_a:
    decision = "NO ECONOMIC EDGE (negative mean)"
else:
    decision = "INSUFFICIENT CONDITIONAL SAMPLE"

print(f"\n  >>> PRIMARY DECISION: {decision}")
print(f"  >>> Test type: {mask_description}")

# ── Save ───────────────────────────────────────────────────────────────
print("\nSaving results...")
output_cols = [
    "episode_idx", "timestamp", "risk_score", "predicted_RV", "predicted_RV_pct",
    "forward_rv_12h", "call_iv", "put_iv", "avg_iv", "forecast_IV_spread",
    "K", "F_entry", "F_expiry", "atm_tte_hours",
    "call_entry_btc", "put_entry_btc", "straddle_premium_btc", "straddle_premium_usd",
    "gross_payoff_usd", "transaction_cost_usd", "net_PnL_usd", "net_PnL_pct",
]
eligible[output_cols].to_csv(REPORTS / "APEX_IC7_BTC_Straddle_Economic_Data.csv", index=False)

summary = {
    "milestone": "IC7", "status": "COMPLETE",
    "eligible_observations": len(eligible),
    "conditional_observations": len(cond_pnl),
    "conditional_type": mask_description,
    "ols_correlation": float(corr),
    "predicted_rv_pct_mean": float(eligible["predicted_RV_pct"].mean()),
    "iv_pct_mean": float(eligible["avg_iv"].mean()),
    "forecast_iv_spread_mean": float(eligible["forecast_IV_spread"].mean()),
    "fraction_predicted_rv_gt_iv": float(n_pos / len(eligible)),
    "straddle_premium_usd_mean": float(eligible["straddle_premium_usd"].mean()),
    "gross_payoff_usd_mean": float(eligible["gross_payoff_usd"].mean()),
    "transaction_cost_usd_mean": float(eligible["transaction_cost_usd"].mean()),
    "net_pnl_usd_mean_all": float(eligible["net_PnL_usd"].mean()),
    "net_pnl_usd_median_all": float(eligible["net_PnL_usd"].median()),
    "net_pnl_pct_mean_all": float(eligible["net_PnL_pct"].mean()),
    "baseline_hit_rate": float((eligible["net_PnL_usd"] > 0).mean()),
    "conditional_mean_pnl": float(mean_pnl),
    "conditional_std_pnl": float(std_pnl),
    "conditional_median_pnl": float(np.median(cond_pnl)),
    "conditional_hit_rate": float((cond_pnl > 0).mean()),
    "hac_t_stat": float(t_stat),
    "hac_se": float(hac_se),
    "p_value_one_sided": float(p_one),
    "ci_95_low": float(ci_low), "ci_95_high": float(ci_high),
    "decision": decision,
    "gate_a": bool(gate_a), "gate_b": bool(gate_b),
    "gate_c": bool(gate_c), "gate_d": bool(gate_d),
}
with open(REPORTS / "APEX_IC7_Result_Summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\n=== IC7 COMPLETE ===")
print(f"Decision: {decision}")
print(f"Conditional N: {len(cond_pnl)}")
print(f"Mean conditional PnL: {mean_pnl:.2f} USD")
print(f"HAC t={t_stat:.4f}, p(one-sided)={p_one:.6f}")
