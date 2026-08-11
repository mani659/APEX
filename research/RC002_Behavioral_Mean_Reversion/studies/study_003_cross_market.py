import os
import sys
import numpy as np
import pandas as pd
from types import MappingProxyType

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from data.loader import load_data
from features.volatility import build_volatility_features

from simulation.market import MarketSnapshot
from simulation.context import TradingContext
from research.features.context import FeatureContext
from research.RC002_Behavioral_Mean_Reversion.features.behavioral_event import BehavioralEventFeature
from research.pipeline.pipeline import FeaturePipeline
from research.store.store import FeatureStore

from research.labeling.context import LabelContext
from research.labels.forward_return import ForwardReturnLabel
from research.labeling.engine import LabelEngine
from research.store.label_store import LabelStore, LabelStoreResult

from research.dataset.builder import build_dataset
from research.experiment.config import ExperimentConfig
from research.splitting.config import SplitConfig
from research.experiment.engine import run as run_experiment

from research.repository.config import RepositoryConfig
from research.repository.engine import ExperimentRepository


def recompute_stats(data):
    a = 1.0 * np.array(data)
    n = len(a)
    if n == 0:
        return {
            "n": 0, "mean": 0, "median": 0, "std": 0, "se": 0,
            "ci_low": 0, "ci_high": 0, "effect_size": 0,
            "win_rate": 0, "expectancy": 0, "skew": 0, "kurt": 0
        }
    m = np.mean(a)
    std = np.std(a, ddof=1) if n > 1 else 0
    se = std / np.sqrt(n) if n > 0 else 0
    ci_low = m - 1.96 * se
    ci_high = m + 1.96 * se
    effect_size = m / std if std != 0 else 0
    
    pos_data = a[a > 0]
    neg_data = a[a < 0]
    win_rate = len(pos_data) / n if n > 0 else 0
    avg_win = np.mean(pos_data) if len(pos_data) > 0 else 0
    avg_loss = np.mean(neg_data) if len(neg_data) > 0 else 0
    expectancy = (win_rate * avg_win) + ((1 - win_rate) * avg_loss)
    
    series = pd.Series(a)
    skew = series.skew()
    kurt = series.kurt()
    
    return {
        "n": n, "mean": m, "median": np.median(a) if n > 0 else 0,
        "std": std, "se": se, "ci_low": ci_low, "ci_high": ci_high,
        "effect_size": effect_size, "win_rate": win_rate,
        "expectancy": expectancy, "skew": skew, "kurt": kurt
    }


def main():
    print("=========================================================")
    print("RC002 Study 003: Cross-Market Behavioral Reproducibility")
    print("=========================================================")
    
    symbols = ["XAUUSD", "XAGUSD", "EURUSD", "BTCUSD", "NAS100"]
    horizons = [5, 10, 20, 40]
    
    all_results = {}
    repo_ids = {}
    
    repo_path = os.path.join(os.path.dirname(__file__), "..", "repository")
    repo_config = RepositoryConfig(repository_path=repo_path, overwrite_existing=True)
    repo = ExperimentRepository(repo_config)
    
    for symbol in symbols:
        print(f"\n[Processing {symbol}]")
        try:
            df = load_data(symbol)
        except Exception as e:
            print(f"Failed to load {symbol}: {e}")
            continue
            
        print("    Computing legacy indicators...")
        vol_features = build_volatility_features(df)
        
        limit = 100000
        if len(df) > limit:
            df = df.tail(limit).reset_index(drop=True)
            vol_features = vol_features.tail(limit).reset_index(drop=True)
            
        num_samples = len(df)
        print(f"    Total usable samples: {num_samples}")

        f_event = BehavioralEventFeature()
        pipeline = FeaturePipeline([f_event])
        f_store = FeatureStore()
        
        labels = [ForwardReturnLabel(horizon=h) for h in horizons]
        label_engine = LabelEngine(labels)
        l_store = LabelStore()
        
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
        volumes = df['volume'].values
        atrs = vol_features['atr'].fillna(1.0).values
        
        snapshots = []
        for i in range(num_samples):
            snapshots.append(MarketSnapshot(
                symbol=symbol, timestamp=int(timestamps[i]), bid=float(closes[i]), ask=float(closes[i]) + 0.05, volume=float(volumes[i])
            ))
        snapshots_tuple = tuple(snapshots)
            
        print("    Running pipelines...")
        max_horizon = max(horizons)
        valid_samples = num_samples - max_horizon
        
        for i in range(valid_samples):
            snap = snapshots_tuple[i]
            
            ind_cache = MappingProxyType({
                "open": float(opens[i]),
                "close": float(closes[i]),
                "atr": float(atrs[i])
            })
            
            f_ctx = FeatureContext(market_snapshot=snap, trading_context=mock_tc, indicator_cache=ind_cache)
            f_res = pipeline.run(f_ctx)
            f_store.add(f_res)
            
            l_ctx = LabelContext(snapshots=snapshots_tuple, index=i)
            l_dict = label_engine.generate(l_ctx)
            l_res = LabelStoreResult(timestamp=snap.timestamp, label_results=MappingProxyType(l_dict))
            l_store.add(l_res)
            
        print(f"    Building Dataset...")
        dataset = build_dataset(f_store, l_store)
        
        data_list = []
        for r in dataset.records:
            d_row = {"event": r.features["behavioral_event_displacement"]}
            for h in horizons:
                d_row[f"ret_{h}"] = r.labels[f"forward_return_{h}"]
            data_list.append(d_row)
            
        df_res = pd.DataFrame(data_list)
        bull_df = df_res[df_res['event'] == 1.0]
        bear_df = df_res[df_res['event'] == -1.0]
        
        sym_res = {}
        for h in horizons:
            col = f"ret_{h}"
            sym_res[h] = {
                "bull": recompute_stats(bull_df[col].dropna()),
                "bear": recompute_stats(bear_df[col].dropna())
            }
            
        all_results[symbol] = sym_res
        
        # Archive
        split_config = SplitConfig(train_ratio=0.6, validation_ratio=0.2, test_ratio=0.2)
        exp_config = ExperimentConfig(
            experiment_name=f"Behavioral_Event_Recoil_{symbol}",
            experiment_version="1.0",
            split_config=split_config
        )
        experiment_record = run_experiment(dataset, exp_config)
        repo_entry = repo.save(experiment_record)
        repo_ids[symbol] = repo_entry.experiment_id


    # Aggregation & Verdict
    print("\n[Aggregating Cross-Market Data]")
    bull_support = 0
    bear_support = 0
    
    # We will measure support primarily at H=20 for the verdict
    h_eval = 20
    for sym in all_results:
        bull = all_results[sym][h_eval]["bull"]
        bear = all_results[sym][h_eval]["bear"]
        
        # Bullish Exhaustion expects negative recoil (mean < 0)
        if bull["mean"] < 0:
            bull_support += 1
            
        # Bearish Exhaustion expects positive recoil (mean > 0)
        if bear["mean"] > 0:
            bear_support += 1
            
    total_markets = len(all_results)
    
    # If 80% (4/5) markets align directionally, we consider it supported.
    if bull_support >= 4 and bear_support >= 4:
        conclusion = "SUPPORTED"
    elif bull_support >= 3 or bear_support >= 3:
        conclusion = "PARTIALLY SUPPORTED"
    else:
        conclusion = "NOT SUPPORTED"
        
    print(f"Final Conclusion: {conclusion}")
    
    # Report Generation
    output_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    report_content = f"""# RC002 Study 003: Cross-Market Behavioral Reproducibility

## Final Research Conclusion
**{conclusion}**

### Target Hypothesis
Does the Behavioral Event (Displacement Exhaustion) produce a consistent directional recoil across independent asset classes?

### Experiment Execution
- **Markets Evaluated**: {', '.join(all_results.keys())}
- **Horizons Evaluated**: 5, 10, 20, 40 bars
- **Dataset Constraint**: Up to 100,000 most recent M1 records per market.

---

## 1. Cross-Market Comparison (Horizon = 20 Bars)

### Bullish Exhaustion Recoil (Expecting Negative Mean)
| Market | Sample Size (N) | Mean Return | Effect Size | 95% CI | Win Rate (Absolute) | Directional Alignment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for sym in all_results:
        stat = all_results[sym][20]["bull"]
        aligned = "✅ Yes" if stat["mean"] < 0 else "❌ No"
        report_content += f"| {sym} | {stat['n']} | {stat['mean']:.5f} | {stat['effect_size']:.3f} | [{stat['ci_low']:.5f}, {stat['ci_high']:.5f}] | {stat['win_rate']*100:.1f}% | {aligned} |\n"
        
    report_content += """
### Bearish Exhaustion Recoil (Expecting Positive Mean)
| Market | Sample Size (N) | Mean Return | Effect Size | 95% CI | Win Rate (Absolute) | Directional Alignment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for sym in all_results:
        stat = all_results[sym][20]["bear"]
        aligned = "✅ Yes" if stat["mean"] > 0 else "❌ No"
        report_content += f"| {sym} | {stat['n']} | {stat['mean']:.5f} | {stat['effect_size']:.3f} | [{stat['ci_low']:.5f}, {stat['ci_high']:.5f}] | {stat['win_rate']*100:.1f}% | {aligned} |\n"

    report_content += """

## 2. Meta Summary & Qualitative Consistency Analysis

### Consistent Markets
- The directional recoil effect following a bearish exhaustion (panic selling) tends to produce a positive mean reversion. 
- Bullish exhaustion (panic buying) tends to produce a negative mean reversion.
"""
    supported_bull = [sym for sym in all_results if all_results[sym][20]["bull"]["mean"] < 0]
    supported_bear = [sym for sym in all_results if all_results[sym][20]["bear"]["mean"] > 0]
    
    report_content += f"- **Markets supporting Bullish Exhaustion Recoil**: {', '.join(supported_bull) if supported_bull else 'None'}\n"
    report_content += f"- **Markets supporting Bearish Exhaustion Recoil**: {', '.join(supported_bear) if supported_bear else 'None'}\n"
    
    report_content += f"""
### Outliers and Contradictory Markets
- Any market where a bullish exhaustion leads to positive forward returns, or bearish exhaustion leads to negative forward returns, indicates the market absorbed the displacement and continued accelerating.
"""
    outlier_bull = [sym for sym in all_results if all_results[sym][20]["bull"]["mean"] >= 0]
    outlier_bear = [sym for sym in all_results if all_results[sym][20]["bear"]["mean"] <= 0]
    
    report_content += f"- **Outliers against Bullish Recoil**: {', '.join(outlier_bull) if outlier_bull else 'None'}\n"
    report_content += f"- **Outliers against Bearish Recoil**: {', '.join(outlier_bear) if outlier_bear else 'None'}\n"

    report_content += f"""
### Verdict
Based on directional alignment at the 20-bar horizon, the hypothesis that behavioral exhaustion is universally reproducible is **{conclusion}**.

---

## 3. Individual Market Reports (All Horizons)

"""
    for sym in all_results:
        report_content += f"### {sym}\n"
        report_content += f"- **Experiment ID**: {repo_ids.get(sym, 'N/A')}\n\n"
        
        report_content += "#### Bullish Exhaustion (Expecting Negative Means)\n"
        for h in horizons:
            stat = all_results[sym][h]["bull"]
            report_content += f"- **H={h}**: N={stat['n']} | Mean={stat['mean']:.4f} | CI=[{stat['ci_low']:.4f}, {stat['ci_high']:.4f}] | Effect={stat['effect_size']:.3f} | Skew={stat['skew']:.2f} | Kurt={stat['kurt']:.2f}\n"
            
        report_content += "\n#### Bearish Exhaustion (Expecting Positive Means)\n"
        for h in horizons:
            stat = all_results[sym][h]["bear"]
            report_content += f"- **H={h}**: N={stat['n']} | Mean={stat['mean']:.4f} | CI=[{stat['ci_low']:.4f}, {stat['ci_high']:.4f}] | Effect={stat['effect_size']:.3f} | Skew={stat['skew']:.2f} | Kurt={stat['kurt']:.2f}\n"
            
        report_content += "\n"

    with open(os.path.join(output_dir, "Study_003_Report.md"), "w", encoding='utf-8') as f:
        f.write(report_content)
        
    print("=========================================================")

if __name__ == "__main__":
    main()
