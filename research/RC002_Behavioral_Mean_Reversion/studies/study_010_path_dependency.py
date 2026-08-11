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
    print("RC002 Study 010: Behavioral Path Dependency")
    print("=========================================================")
    
    symbols = ["XAUUSD"]
    horizons = [5, 20]
    all_data = []
    
    for symbol in symbols:
        print(f"\n[Loading Data for {symbol}]")
        df = load_data(symbol)
        
        print("    Computing indicators...")
        vol_features = build_volatility_features(df)
        df['volume_percentile'] = df['volume'].rolling(window=500).rank(pct=True)
        
        df['body'] = df['close'] - df['open']
        df['sign'] = np.sign(df['body'])
        df['tr'] = vol_features['atr'] # Approximation for speed, assuming ATR is already TR-smoothed.
        
        # Pre-event sequence (Shift 1 to exclude the event candle itself)
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
            
            ind_cache = MappingProxyType({
                "open": float(opens[i]),
                "close": float(closes[i]),
                "atr": float(atr_val),
                "volume_percentile": float(vol_pcts[i]),
                "event_val": float(event_val),
                "prev_5_dir": float(p5d[i] * event_val), # Align sign so + is same direction
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
            
            f_res = f_seq[i]
            path_data = f_res.feature_results["behavioral_path_data"].metadata if "behavioral_path_data" in f_res.feature_results else {}
            
            homog = path_data.get("homogeneity", 0.0)
            expans = path_data.get("expansion", 1.0)
            vslope = path_data.get("vol_slope", 0.0)
            
            homog_class = "High" if homog >= 0.6 else ("Low" if homog <= -0.6 else "Mixed")
            expans_class = "Sudden" if expans < 1.2 else "Gradual"
            vslope_class = "Building" if vslope > 0.1 else ("Fading" if vslope < -0.1 else "Flat")
            
            response = classify_response(event_val, ret_5, ret_20, atr)
            
            all_data.append({
                "symbol": symbol,
                "homogeneity": homog_class,
                "expansion": expans_class,
                "vol_slope": vslope_class,
                "response": response
            })

    df_res = pd.DataFrame(all_data)
    total_events = len(df_res)
    
    print(f"\nTotal Exhaustion Events Analyzed: {total_events}")
    categories = ["Immediate Recoil", "Delayed Recoil", "Momentum Continuation", "Volatility Absorption"]
    
    base_counts = df_res['response'].value_counts()
    base_arr = [base_counts.get(c, 0) for c in categories]
    base_entropy = calculate_entropy(base_arr)
    print(f"\nBaseline Entropy: {base_entropy:.4f}")
    
    def analyze_descriptor(name, column):
        print(f"\n--- {name} ---")
        vals = df_res[column].unique()
        for v in vals:
            df_sub = df_res[df_res[column] == v]
            c = [df_sub['response'].value_counts().get(cat, 0) for cat in categories]
            ent = calculate_entropy(c)
            red = (base_entropy - ent) / base_entropy * 100 if base_entropy > 0 else 0
            print(f"  {v} (N={len(df_sub)}): Entropy {ent:.4f} (Reduction: {red:+.2f}%)")
            
    analyze_descriptor("Sequence Homogeneity", "homogeneity")
    analyze_descriptor("Expansion Profile", "expansion")
    analyze_descriptor("Participation Evolution", "vol_slope")
    
    print("\n=========================================================")

if __name__ == "__main__":
    main()
