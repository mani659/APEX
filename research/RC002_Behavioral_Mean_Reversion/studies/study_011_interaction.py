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

def calculate_entropy(counts):
    total = sum(counts)
    if total == 0:
        return 0.0
    entropy = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            entropy -= p * math.log2(p)
    return entropy

def classify_response(event_val, ret_5, ret_20, atr):
    if event_val == 0.0:
        return None
    expected_dir = -1.0 if event_val == 1.0 else 1.0
    recoil_5 = ret_5 * expected_dir
    recoil_20 = ret_20 * expected_dir
    threshold = atr * 1.0
    
    if recoil_5 > threshold:
        return "Immediate Recoil"
    elif recoil_20 > threshold:
        return "Delayed Recoil"
    elif recoil_20 < -threshold:
        return "Momentum Continuation"
    else:
        return "Volatility Absorption"

def main():
    print("=========================================================")
    print("RC002 Study 011: Participation x Expansion Interaction")
    print("=========================================================")
    
    symbols = ["XAUUSD", "XAGUSD", "EURUSD", "BTCUSD", "NAS100"]
    horizons = [5, 20]
    all_data = []
    
    repo_path = os.path.join(os.path.dirname(__file__), "..", "repository")
    repo_config = RepositoryConfig(repository_path=repo_path, overwrite_existing=True)
    repo = ExperimentRepository(repo_config)
    
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

        limit = 300000
        if len(df) > limit:
            df = df.tail(limit).reset_index(drop=True)
            vol_features = vol_features.tail(limit).reset_index(drop=True)
        
        print("    Computing indicators...")
        vol_features = build_volatility_features(df)
        df['volume_percentile'] = df['volume'].rolling(window=500).rank(pct=True)
        
        df['body'] = df['close'] - df['open']
        df['sign'] = np.sign(df['body'])
        df['tr'] = vol_features['atr'] # Approximation
        
        # Pre-event sequence
        df['prev_5_dir'] = df['sign'].shift(1).rolling(5).sum()
        df['prev_5_atr'] = df['tr'].shift(1).rolling(5).mean()
        df['prev_15_atr'] = df['tr'].shift(6).rolling(15).mean()
        df['prev_10_vol_slope'] = df['volume_percentile'].shift(1) - df['volume_percentile'].shift(11)
        

        num_samples = len(df)
        print(f"    Total usable samples: {num_samples}")

        f_event = BehavioralEventFeature()
        f_part = ParticipationStateFeature()
        f_path = BehavioralPathFeature()
        pipeline = FeaturePipeline([f_event, f_part, f_path])
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
            
        print("    Running pipelines...")
        max_horizon = max(horizons)
        valid_samples = num_samples - max_horizon
        
        for i in range(valid_samples):
            snap = snapshots_tuple[i]
            
            atr_val = atrs[i] if atrs[i] > 0 else 1.0
            body_size = abs(closes[i] - opens[i])
            event_val = 0.0
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
            f_store.add(f_res)
            
            l_ctx = LabelContext(snapshots=snapshots_tuple, index=i)
            l_dict = label_engine.generate(l_ctx)
            l_res = LabelStoreResult(timestamp=snap.timestamp, label_results=MappingProxyType(l_dict))
            l_store.add(l_res)
            
        print(f"    Building Dataset...")
        dataset = build_dataset(f_store, l_store)
        f_seq = f_store.get_all()
        
        for i, r in enumerate(dataset.records):
            event_val = r.features.get("behavioral_event_displacement", 0.0)
            if event_val == 0.0:
                continue
                
            ret_5 = r.labels["forward_return_5"]
            ret_20 = r.labels["forward_return_20"]
            atr = atrs[i] if atrs[i] > 0 else 1.0
            
            part_val = r.features.get("participation_state", 0.0)
            is_low_part = (part_val == -1.0)
            
            f_res = f_seq[i]
            path_data = f_res.feature_results["behavioral_path_data"].metadata if "behavioral_path_data" in f_res.feature_results else {}
            expans = path_data.get("expansion", 1.0)
            is_gradual = (expans >= 1.2)
            
            if is_low_part and is_gradual:
                group = "Low Part + Gradual Expansion"
            elif is_low_part and not is_gradual:
                group = "Low Part + Sudden Shock"
            elif not is_low_part and is_gradual:
                group = "Normal Part + Gradual Expansion"
            else:
                group = "Normal Part + Sudden Shock"
            
            response = classify_response(event_val, ret_5, ret_20, atr)
            
            all_data.append({
                "symbol": symbol,
                "group": group,
                "is_low_part": is_low_part,
                "is_gradual": is_gradual,
                "response": response
            })
            
        print(f"    Archiving Experiment...")
        split_config = SplitConfig(train_ratio=0.6, validation_ratio=0.2, test_ratio=0.2)
        exp_config = ExperimentConfig(
            experiment_name=f"Study_011_Interaction_{symbol}",
            experiment_version="1.0",
            split_config=split_config
        )
        experiment_record = run_experiment(dataset, exp_config)
        repo.save(experiment_record)

    df_res = pd.DataFrame(all_data)
    total_events = len(df_res)
    
    print(f"\nTotal Exhaustion Events Analyzed: {total_events}")
    categories = ["Immediate Recoil", "Delayed Recoil", "Momentum Continuation", "Volatility Absorption"]
    
    base_counts = df_res['response'].value_counts()
    base_arr = [base_counts.get(c, 0) for c in categories]
    base_entropy = calculate_entropy(base_arr)
    print(f"\nBaseline Entropy: {base_entropy:.4f}")
    
    # 007 Isolation
    df_low = df_res[df_res['is_low_part']]
    low_counts = [df_low['response'].value_counts().get(c, 0) for c in categories]
    low_ent = calculate_entropy(low_counts)
    print(f"Study 007 Base (Low Part Only) N={len(df_low)}: Entropy {low_ent:.4f} (Red: {(base_entropy - low_ent)/base_entropy*100:.2f}%)")
    
    # 010 Isolation
    df_grad = df_res[df_res['is_gradual']]
    grad_counts = [df_grad['response'].value_counts().get(c, 0) for c in categories]
    grad_ent = calculate_entropy(grad_counts)
    print(f"Study 010 Base (Gradual Exp Only) N={len(df_grad)}: Entropy {grad_ent:.4f} (Red: {(base_entropy - grad_ent)/base_entropy*100:.2f}%)")
    
    groups = [
        "Low Part + Gradual Expansion",
        "Low Part + Sudden Shock",
        "Normal Part + Gradual Expansion",
        "Normal Part + Sudden Shock"
    ]
    
    report = f"# RC002 Study 011: Interaction Matrix Report\n\n"
    report += "## Entropy Comparison Table\n\n"
    report += "| Context | Entropy | Reduction |\n"
    report += "| :--- | :--- | :--- |\n"
    report += f"| Baseline (Unconditioned) | {base_entropy:.4f} | 0.00% |\n"
    report += f"| Study 007 Baseline (Low Part Only) | {low_ent:.4f} | {(base_entropy - low_ent)/base_entropy*100 if base_entropy > 0 else 0:.2f}% |\n"
    report += f"| Study 010 Baseline (Gradual Exp Only) | {grad_ent:.4f} | {(base_entropy - grad_ent)/base_entropy*100 if base_entropy > 0 else 0:.2f}% |\n\n"
    
    report += "## Interaction Matrix\n\n"
    report += "This table shows the combined synergistic effect of both variables.\n\n"
    report += "| Interaction Group | Sample Count | Shannon Entropy | Relative Entropy Reduction |\n"
    report += "| :--- | :--- | :--- | :--- |\n"
    
    matrix_data = []
    
    print("\n--- Interaction Matrix ---")
    for g in groups:
        df_g = df_res[df_res['group'] == g]
        count = len(df_g)
        if count == 0:
            matrix_data.append((g, 0, 0.0, 0.0, []))
            report += f"| {g} | {count} | N/A | N/A |\n"
            continue
        c = [df_g['response'].value_counts().get(cat, 0) for cat in categories]
        ent = calculate_entropy(c)
        red = (base_entropy - ent) / base_entropy * 100 if base_entropy > 0 else 0
        
        matrix_data.append((g, count, ent, red, c))
        report += f"| {g} | {count} | {ent:.4f} | {red:+.2f}% |\n"
        
        print(f"{g} (N={count})")
        print(f"  Entropy: {ent:.4f} (Reduction: {red:+.2f}%)")
        print(f"  Class Distribution: {c}")
        
    report += "\n## Transition Matrices (Class Distribution)\n\n"
    report += "| Interaction Group | Immediate Recoil | Delayed Recoil | Momentum Continuation | Volatility Absorption |\n"
    report += "| :--- | :--- | :--- | :--- | :--- |\n"
    for g, count, ent, red, c in matrix_data:
        if count == 0:
            continue
        report += f"| {g} | {c[0]} ({(c[0]/count*100):.1f}%) | {c[1]} ({(c[1]/count*100):.1f}%) | {c[2]} ({(c[2]/count*100):.1f}%) | {c[3]} ({(c[3]/count*100):.1f}%) |\n"
    
    report += "\n"
        
    print("\n=========================================================")
    
    output_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    with open(os.path.join(output_dir, "Study_011_Report.md"), "w", encoding="utf-8") as f:
        f.write(report)
        
if __name__ == "__main__":
    main()
