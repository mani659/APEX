import os
import sys
import numpy as np
import pandas as pd
from types import MappingProxyType
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from data.loader import load_data
from features.volatility import build_volatility_features
from simulation.market import MarketSnapshot
from simulation.context import TradingContext
from research.features.context import FeatureContext
from research.RC002_Behavioral_Mean_Reversion.features.behavioral_event import BehavioralEventFeature
from research.RC002_Behavioral_Mean_Reversion.features.participation_state import ParticipationStateFeature
from research.RC002_Behavioral_Mean_Reversion.features.behavioral_path import BehavioralPathFeature
from research.pipeline.pipeline import FeaturePipeline

def main():
    print("=========================================================")
    print("RC002 Study 012: Execution Policy Evaluation")
    print("=========================================================")
    
    symbols = ["XAUUSD", "XAGUSD", "EURUSD", "BTCUSD", "NAS100"]
    
    results = []

    for symbol in symbols:
        print(f"\n[Loading Data for {symbol}]")
        try:
            df = load_data(symbol)
        except Exception as e:
            print(f"Failed to load {symbol}: {e}")
            continue
            
        print("    Computing indicators...")
        vol_features = build_volatility_features(df)
        df['volume_percentile'] = df['volume'].rolling(window=500).rank(pct=True)
        
        df['body'] = df['close'] - df['open']
        df['sign'] = np.sign(df['body'])
        df['tr'] = vol_features['atr'] # Approximation
        
        df['prev_5_dir'] = df['sign'].shift(1).rolling(5).sum()
        df['prev_5_atr'] = df['tr'].shift(1).rolling(5).mean()
        df['prev_15_atr'] = df['tr'].shift(6).rolling(15).mean()
        df['prev_10_vol_slope'] = df['volume_percentile'].shift(1) - df['volume_percentile'].shift(11)
        
        limit = 300000
        if len(df) > limit:
            df = df.tail(limit).reset_index(drop=True)
            vol_features = vol_features.tail(limit).reset_index(drop=True)
            
        num_samples = len(df)
        print(f"    Total usable samples: {num_samples}")

        f_event = BehavioralEventFeature()
        f_part = ParticipationStateFeature()
        f_path = BehavioralPathFeature()
        pipeline = FeaturePipeline([f_event, f_part, f_path])
        
        mock_tc = TradingContext(
            timestamp=0, bar_index=0, session="NYC", day_of_week=1, market_open=True,
            current_price=100.0, spread=0.05, volatility_regime="LOW", trend_regime="FLAT",
            market_structure="RANGE", atr=1.0, equity=10000.0, balance=10000.0,
            floating_pnl=0.0, closed_pnl=0.0, drawdown=0.0, daily_pnl=0.0, max_drawdown=0.0,
            open_positions=0, long_positions=0, short_positions=0, net_exposure=0.0,
            margin_used=0.0, available_margin=10000.0, daily_loss_limit_hit=False,
            risk_enabled=True, max_positions_reached=False, trading_paused=False,
            last_fill_price=0.0, last_slippage=0.0, last_commission=0.0, last_trade_time=0
        )
        
        timestamps = ((df['datetime'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1s')).values
        opens = df['open'].values
        closes = df['close'].values
        highs = df['high'].values
        lows = df['low'].values
        volumes = df['volume'].values
        vol_pcts = df['volume_percentile'].bfill().fillna(0.5).values
        atrs = vol_features['atr'].fillna(1.0).values
        
        p5d = df['prev_5_dir'].fillna(0.0).values
        p5a = df['prev_5_atr'].fillna(1.0).values
        p15a = df['prev_15_atr'].fillna(1.0).values
        pv10 = df['prev_10_vol_slope'].fillna(0.0).values
        
        snapshots = []
        for i in range(num_samples):
            snapshots.append(MarketSnapshot(
                symbol=symbol, timestamp=int(timestamps[i]), bid=float(closes[i]), ask=float(closes[i]) + 0.05, volume=float(volumes[i])
            ))
        snapshots_tuple = tuple(snapshots)
            
        print("    Evaluating events & policies...")
        
        for i in range(num_samples - 60):
            snap = snapshots_tuple[i]
            
            atr_val = atrs[i] if atrs[i] > 0 else 1.0
            body_size = abs(closes[i] - opens[i])
            
            if body_size > 3.0 * atr_val:
                event_val = 1.0 if closes[i] > opens[i] else -1.0
            else:
                continue
            
            ind_cache = MappingProxyType({
                "open": float(opens[i]),
                "close": float(closes[i]),
                "atr": float(atr_val),
                "volume_percentile": float(vol_pcts[i]),
                "event_val": float(event_val),
                "prev_5_dir": float(p5d[i] * event_val),
                "prev_5_atr": float(p5a[i]),
                "prev_15_atr": float(p15a[i]),
                "prev_10_vol_slope": float(pv10[i])
            })
            
            f_ctx = FeatureContext(market_snapshot=snap, trading_context=mock_tc, indicator_cache=ind_cache)
            f_res = pipeline.run(f_ctx)
            
            # Context: Low Part + Sudden Shock
            if "participation_state" not in f_res.feature_results:
                continue
            if f_res.feature_results["participation_state"].value != -1.0:
                continue
                
            if "behavioral_path_data" not in f_res.feature_results:
                continue
            path_data = f_res.feature_results["behavioral_path_data"].metadata
            expans = path_data.get("expansion", 1.0)
            is_gradual = (expans >= 1.2)
            if is_gradual:
                continue
                
            trade_dir = -1 if event_val == 1.0 else 1
            event_high = highs[i]
            event_low = lows[i]
            event_open = opens[i]
            
            entries = {}
            entries['Policy A (Immediate)'] = {'idx': i, 'price': closes[i]}
            
            next_idx = i + 1
            if next_idx < num_samples:
                b_body = closes[next_idx] - opens[next_idx]
                if (trade_dir == 1 and b_body > 0) or (trade_dir == -1 and b_body < 0):
                    entries['Policy B (One-bar Conf.)'] = {'idx': next_idx, 'price': closes[next_idx]}
            
            for j in range(1, 11):
                idx = i + j
                if idx >= num_samples: break
                c_body = abs(closes[idx] - opens[idx])
                if c_body < 0.5 * atrs[idx]:
                    entries['Policy C (Absorption)'] = {'idx': idx, 'price': closes[idx]}
                    break
                    
            for j in range(1, 11):
                idx = i + j
                if idx >= num_samples: break
                breached = False
                closed_within = False
                if trade_dir == -1:
                    if highs[idx] > event_high:
                        breached = True
                        if closes[idx] <= event_high:
                            closed_within = True
                else:
                    if lows[idx] < event_low:
                        breached = True
                        if closes[idx] >= event_low:
                            closed_within = True
                            
                if breached and closed_within:
                    entries['Policy D (Fade Failure)'] = {'idx': idx, 'price': closes[idx]}
                    break
                    
            for p_name, p_entry in entries.items():
                e_idx = p_entry['idx']
                e_price = p_entry['price']
                e_atr = atrs[e_idx]
                
                exit_results = {}
                
                # Fixed 20
                ex_idx = min(e_idx + 20, num_samples - 1)
                pnl = (closes[ex_idx] - e_price) * trade_dir
                exit_results['Fixed 20 Bars'] = {'pnl': pnl, 'bars': ex_idx - e_idx}
                
                # ATR Target
                sl_price = e_price - (trade_dir * e_atr)
                tp_price = e_price + (trade_dir * e_atr)
                hit_exit = False
                for j in range(e_idx + 1, min(e_idx + 61, num_samples)):
                    h = highs[j]
                    l = lows[j]
                    hit_sl = (trade_dir == 1 and l <= sl_price) or (trade_dir == -1 and h >= sl_price)
                    hit_tp = (trade_dir == 1 and h >= tp_price) or (trade_dir == -1 and l <= tp_price)
                    
                    if hit_sl and hit_tp:
                        exit_results['ATR Target'] = {'pnl': -e_atr, 'bars': j - e_idx}
                        hit_exit = True
                        break
                    elif hit_sl:
                        exit_results['ATR Target'] = {'pnl': -e_atr, 'bars': j - e_idx}
                        hit_exit = True
                        break
                    elif hit_tp:
                        exit_results['ATR Target'] = {'pnl': e_atr, 'bars': j - e_idx}
                        hit_exit = True
                        break
                
                if not hit_exit:
                    ex_idx = min(e_idx + 60, num_samples - 1)
                    exit_results['ATR Target'] = {'pnl': (closes[ex_idx] - e_price) * trade_dir, 'bars': ex_idx - e_idx}
                    
                # Recoil Completion
                hit_exit = False
                for j in range(e_idx + 1, min(e_idx + 61, num_samples)):
                    h = highs[j]
                    l = lows[j]
                    crossed = (trade_dir == 1 and h >= event_open) or (trade_dir == -1 and l <= event_open)
                    if crossed:
                        pnl = (event_open - e_price) * trade_dir
                        exit_results['Recoil Completion'] = {'pnl': pnl, 'bars': j - e_idx}
                        hit_exit = True
                        break
                
                if not hit_exit:
                    ex_idx = min(e_idx + 60, num_samples - 1)
                    exit_results['Recoil Completion'] = {'pnl': (closes[ex_idx] - e_price) * trade_dir, 'bars': ex_idx - e_idx}
                    
                # Time 60
                ex_idx = min(e_idx + 60, num_samples - 1)
                pnl = (closes[ex_idx] - e_price) * trade_dir
                exit_results['Time 60 Bars'] = {'pnl': pnl, 'bars': ex_idx - e_idx}
                
                # MFE / MAE
                max_bars_held = max([r['bars'] for r in exit_results.values()])
                mfe = 0.0
                mae = 0.0
                for j in range(e_idx + 1, e_idx + max_bars_held + 1):
                    if j >= num_samples: break
                    if trade_dir == 1:
                        bar_mfe = highs[j] - e_price
                        bar_mae = lows[j] - e_price
                    else:
                        bar_mfe = e_price - lows[j]
                        bar_mae = e_price - highs[j]
                        
                    if bar_mfe > mfe: mfe = bar_mfe
                    if bar_mae < mae: mae = bar_mae
                    
                for ex_name, ex_res in exit_results.items():
                    results.append({
                        'symbol': symbol,
                        'policy': p_name,
                        'exit': ex_name,
                        'pnl_r': ex_res['pnl'] / e_atr,
                        'bars': ex_res['bars'],
                        'mfe_r': mfe / e_atr,
                        'mae_r': mae / e_atr
                    })

    # Analysis and reporting
    df_res = pd.DataFrame(results)
    
    report = "# RC002 Study 012: Execution Policy Evaluation\n\n"
    report += "This report evaluates whether the execution policy materially impacts the profitability of the 'Low Participation + Sudden Shock' Behavioral Event.\n\n"
    
    policies = ["Policy A (Immediate)", "Policy B (One-bar Conf.)", "Policy C (Absorption)", "Policy D (Fade Failure)"]
    exits = ["Fixed 20 Bars", "ATR Target", "Recoil Completion", "Time 60 Bars"]
    
    report += "## 1. Policy Comparison (Aggregated across all Exits)\n\n"
    report += "| Execution Policy | N | Win Rate | Mean Return (R) | Profit Factor | Exp (R) | Avg Hold (Bars) |\n"
    report += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    best_exp = -999.0
    best_policy = "None"
    best_robustness = False
    
    for p in policies:
        df_p = df_res[df_res['policy'] == p]
        if len(df_p) == 0:
            report += f"| {p} | 0 | N/A | N/A | N/A | N/A | N/A |\n"
            continue
            
        n = len(df_p)
        wins = df_p[df_p['pnl_r'] > 0]
        losses = df_p[df_p['pnl_r'] <= 0]
        
        wr = len(wins) / n * 100
        mean_ret = df_p['pnl_r'].mean()
        
        gross_profit = wins['pnl_r'].sum()
        gross_loss = abs(losses['pnl_r'].sum())
        pf = gross_profit / gross_loss if gross_loss > 0 else 99.99
        exp = mean_ret
        avg_hold = df_p['bars'].mean()
        
        report += f"| {p} | {n} | {wr:.1f}% | {mean_ret:.3f} | {pf:.2f} | {exp:.3f} | {avg_hold:.1f} |\n"
        
        if exp > best_exp:
            best_exp = exp
            best_policy = p
            best_robustness = n > 100
            
    report += "\n## 2. Granular Comparison Matrix\n\n"
    for ex in exits:
        report += f"### Exit: {ex}\n\n"
        report += "| Execution Policy | N | Win Rate | Mean Return (R) | Profit Factor | Max Favorable (R) | Max Adverse (R) |\n"
        report += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        
        df_ex = df_res[df_res['exit'] == ex]
        for p in policies:
            df_pex = df_ex[df_ex['policy'] == p]
            if len(df_pex) == 0:
                report += f"| {p} | 0 | N/A | N/A | N/A | N/A | N/A |\n"
                continue
                
            n = len(df_pex)
            wins = df_pex[df_pex['pnl_r'] > 0]
            losses = df_pex[df_pex['pnl_r'] <= 0]
            wr = len(wins) / n * 100
            mean_ret = df_pex['pnl_r'].mean()
            gross_profit = wins['pnl_r'].sum()
            gross_loss = abs(losses['pnl_r'].sum())
            pf = gross_profit / gross_loss if gross_loss > 0 else 99.99
            
            mfe = df_pex['mfe_r'].mean()
            mae = df_pex['mae_r'].mean()
            
            report += f"| {p} | {n} | {wr:.1f}% | {mean_ret:.3f} | {pf:.2f} | {mfe:.2f} | {mae:.2f} |\n"
        report += "\n"

    # Conclusion Logic
    if best_exp > 0.1 and best_robustness:
        conclusion = "SUPPORTED"
    elif best_exp > 0.05:
        conclusion = "FRAGILE"
    else:
        conclusion = "NOT SUPPORTED"
        
    report += f"## Final Verdict\n\n**{conclusion}**\n\n"
    
    if conclusion == "SUPPORTED":
        report += f"Execution policy materially impacts outcomes, with **{best_policy}** showing robust outperformance."
    elif conclusion == "FRAGILE":
        report += f"**{best_policy}** showed some outperformance, but lacks the statistical robustness (N < 100 or low expectancy) to confirm."
    else:
        report += "Execution policy modifications did not materially yield robust profitability on this event class. The structural edge is either absent or highly susceptible to noise."

    output_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    with open(os.path.join(output_dir, "Study_012_Report.md"), "w", encoding='utf-8') as f:
        f.write(report)
        
    print(f"Report generated: Study_012_Report.md")
    print(f"Final Verdict: {conclusion}")

if __name__ == "__main__":
    main()
