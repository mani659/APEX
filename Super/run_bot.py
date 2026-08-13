#!/usr/bin/env python3
"""
ML-SuperTrend-MT5 Bot Runner — v2.2
=====================================
Author: xPOURY4

Changes from v2.1 runner
-------------------------
- Imports from supertrend_bot (canonical module name)
- place_order no longer accepts a price argument (tick fetched internally)
- New CLI flags:
    --equity-filter          Enable equity curve filter (default: off)
    --equity-filter-period   Rolling window in cycles (default: 20)
    --equity-filter-ratio    Pause threshold ratio (default: 0.97)
    --partial-close          Enable partial close on extreme SI (default: off)
    --partial-close-si       SI threshold for partial close (default: 0.85)
    --partial-close-atr      ATR-profit multiple required (default: 3.0)
    --partial-close-frac     Fraction of volume to close (default: 0.50)
- build_config() maps all new v2.2 Config fields from config.json
- Dynamic incubation fields (incubation_bars_trending/stable/exhaustion)
  are now read from config.json per-symbol

Usage examples
--------------
Single symbol, no new features:
    python run_bot.py --symbol EURUSDm

Multi-pair with equity filter:
    python run_bot.py --symbols EURUSDm,GBPUSDm --equity-filter

Multi-pair with partial close (50% at 3 ATR profit, SI >= 0.85):
    python run_bot.py --symbols EURUSDm,GBPUSDm --partial-close

Full demo — dry run, equity filter, partial close:
    python run_bot.py --symbols EURUSDm,GBPUSDm,XAUUSDm \\
        --dry-run --equity-filter --partial-close --monitor
"""

import sys
import json
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path

try:
    import MetaTrader5 as mt5
except ImportError:
    print("Error: MetaTrader5 module not found.")
    print("Please install it using: pip install MetaTrader5")
    sys.exit(1)

from supertrend_bot import SuperTrendBot, Config, MultiPairRunner


# ==============================================================================
#  LOGGING
# ==============================================================================
def setup_logging(log_level: str = "INFO") -> logging.Logger:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.FileHandler(
                f"logs/bot_{datetime.now().strftime('%Y%m%d')}.log"
            ),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger(__name__)


# ==============================================================================
#  CONFIG LOADER
# ==============================================================================
def load_config(config_file: str = "config/config.json") -> dict:
    config_path = Path(config_file)
    if not config_path.exists():
        print(f"Error: Configuration file '{config_file}' not found.")
        print("Please copy config.example.json to config.json and update it.")
        sys.exit(1)
    with open(config_path, "r") as f:
        return json.load(f)


# ==============================================================================
#  ARGUMENT PARSER
# ==============================================================================
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="ML-SuperTrend Trading Bot v2.2 for MetaTrader 5",
        epilog="Example: python run_bot.py --symbols EURUSDm,GBPUSDm --equity-filter --dry-run",
    )

    # ── Account ───────────────────────────────────────────────────────────────
    parser.add_argument(
        "--account", default="demo", choices=["demo", "live"],
        help="Account type (default: demo)",
    )

    # ── Symbol selection ──────────────────────────────────────────────────────
    sym_group = parser.add_mutually_exclusive_group()
    sym_group.add_argument(
        "--symbol", default=None,
        help="Single trading symbol (e.g. EURUSDm)",
    )
    sym_group.add_argument(
        "--symbols", default=None,
        help="Comma-separated list of symbols (e.g. EURUSDm,GBPUSDm,XAUUSDm)",
    )

    # ── Global position cap ───────────────────────────────────────────────────
    parser.add_argument(
        "--max-total-positions", type=int, default=5,
        help="Max open positions across ALL symbols combined (default: 5)",
    )

    # ── Runtime ───────────────────────────────────────────────────────────────
    parser.add_argument(
        "--config", default="config/config.json",
        help="Configuration file path (default: config/config.json)",
    )
    parser.add_argument(
        "--interval", type=int, default=30,
        help="Update interval in seconds (default: 30)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Simulation mode — no real trades placed",
    )
    parser.add_argument(
        "--backtest", action="store_true",
        help="Run backtest instead of live trading",
    )
    parser.add_argument(
        "--monitor", action="store_true",
        help="Print per-symbol statistics on shutdown",
    )
    parser.add_argument(
        "--log-level", default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )

    # ── v2.2: Equity Curve Filter ─────────────────────────────────────────────
    eq = parser.add_argument_group("Equity Curve Filter (v2.2)")
    eq.add_argument(
        "--equity-filter", action="store_true",
        help="Enable equity curve filter (pauses new entries on drawdown)",
    )
    eq.add_argument(
        "--equity-filter-period", type=int, default=20, metavar="N",
        help="Rolling window in cycles for equity average (default: 20)",
    )
    eq.add_argument(
        "--equity-filter-ratio", type=float, default=0.97, metavar="R",
        help="Pause entries if equity < R × rolling average (default: 0.97)",
    )

    # ── v2.2: Partial Close ───────────────────────────────────────────────────
    pc = parser.add_argument_group("Partial Close (v2.2)")
    pc.add_argument(
        "--partial-close", action="store_true",
        help="Enable one-time partial close when SI is extreme and trade is in profit",
    )
    pc.add_argument(
        "--partial-close-si", type=float, default=0.85, metavar="SI",
        help="SI threshold required for partial close (default: 0.85)",
    )
    pc.add_argument(
        "--partial-close-atr", type=float, default=3.0, metavar="MULT",
        help="Profit in ATR multiples required for partial close (default: 3.0)",
    )
    pc.add_argument(
        "--partial-close-frac", type=float, default=0.50, metavar="FRAC",
        help="Fraction of volume to partially close (default: 0.50 = 50%%)",
    )

    return parser.parse_args()


# ==============================================================================
#  MT5 CONNECTION
# ==============================================================================
def connect_mt5(login: int, password: str, server: str, logger):
    if not mt5.initialize(timeout=180000):
        logger.error(f"MT5 initialize failed: {mt5.last_error()}")
        return None
    if not mt5.login(login, password=password, server=server):
        error = mt5.last_error()
        mt5.shutdown()
        logger.error(f"Login failed: {error}")
        return None
    account_info = mt5.account_info()
    if account_info is None:
        mt5.shutdown()
        logger.error("Failed to get account info")
        return None
    return account_info


# ==============================================================================
#  TIMEFRAME MAP
# ==============================================================================
TIMEFRAME_MAP = {
    "M1":  mt5.TIMEFRAME_M1,
    "M5":  mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1":  mt5.TIMEFRAME_H1,
    "H4":  mt5.TIMEFRAME_H4,
    "D1":  mt5.TIMEFRAME_D1,
}


# ==============================================================================
#  CONFIG BUILDER
#  Priority: CLI flags > per-symbol config.json > global_settings > defaults
# ==============================================================================
def build_config(symbol: str, config_data: dict, args) -> Config:
    """
    Build a v2.2 Config for one symbol.

    Reading order (highest priority first):
      1. CLI flags  (--partial-close, --partial-close-si, etc.)
      2. Per-symbol block in config.json  ["symbols"]["EURUSDm"]
      3. Global settings block            ["global_settings"]
      4. Config dataclass defaults

    config.json per-symbol block supports all v2.2 fields, e.g.:
    {
      "symbols": {
        "XAUUSDm": {
          "enabled": true,
          "timeframe": "M30",
          "risk_percent": 0.5,
          "si_weight_volume": 0.25,
          "si_weight_cluster": 0.30,
          "si_weight_regime": 0.25,
          "si_weight_adx": 0.20,
          "incubation_bars_trending": 1,
          "incubation_bars_stable": 2,
          "incubation_bars_exhaustion": 4,
          "enable_partial_close": true,
          "si_partial_close_min": 0.88,
          "partial_close_profit_atr_mult": 2.5,
          "partial_close_fraction": 0.50
        }
      }
    }
    """
    gs  = config_data.get("global_settings", {})
    sym = config_data.get("symbols", {}).get(symbol, {})

    def get(sym_key, gs_key=None, default=None):
        if sym_key in sym:
            return sym[sym_key]
        k = gs_key or sym_key
        if k in gs:
            return gs[k]
        return default

    # Partial close: CLI flag takes precedence, then per-symbol config
    enable_pc = args.partial_close or bool(get("enable_partial_close", default=False))

    return Config(
        # ── Identity ──────────────────────────────────────────────────────────
        symbol    = symbol,
        timeframe = TIMEFRAME_MAP.get(get("timeframe", default="M30"), mt5.TIMEFRAME_M30),

        # ── K-Means SuperTrend ────────────────────────────────────────────────
        atr_period     = get("atr_period",      "atr_period",        10),
        min_factor     = get("min_factor",                            1.0),
        max_factor     = get("max_factor",                            5.0),
        factor_step    = get("factor_step",                           0.5),
        perf_alpha     = get("perf_alpha",       "performance_alpha", 10.0),
        cluster_choice = get("cluster_choice",                        "Best"),

        # ── Volume gate ───────────────────────────────────────────────────────
        volume_ma_period  = get("volume_ma_period",  "volume_ma_period", 20),
        volume_multiplier = get("volume_multiplier",                      1.2),

        # ── Risk ──────────────────────────────────────────────────────────────
        risk_percent  = get("risk_percent",                          1.0),
        max_positions = get("max_positions", "max_positions_per_symbol", 1),
        magic_number  = get("magic_number",  "magic_number",        123456),

        # ── SL / TP ───────────────────────────────────────────────────────────
        sl_multiplier        = get("sl_multiplier",            2.0),
        tp_safety_multiplier = get("tp_multiplier",            10.0),  # legacy key

        # ── Dynamic Incubation (v2.2) ─────────────────────────────────────────
        incubation_bars            = get("incubation_bars",             "incubation_bars",            2),
        incubation_bars_trending   = get("incubation_bars_trending",    "incubation_bars_trending",   1),
        incubation_bars_stable     = get("incubation_bars_stable",      "incubation_bars_stable",     2),
        incubation_bars_exhaustion = get("incubation_bars_exhaustion",  "incubation_bars_exhaustion", 3),

        # ── State Machine ─────────────────────────────────────────────────────
        si_confirmed            = get("si_confirmed",           "si_confirmed",            0.65),
        si_decaying             = get("si_decaying",            "si_decaying",             0.50),
        si_dead                 = get("si_dead",                "si_dead",                 0.35),
        er_confirmed            = get("er_confirmed",           "er_confirmed",            0.35),
        er_dead                 = get("er_dead",                "er_dead",                 0.20),
        er_bars_for_dead        = get("er_bars_for_dead",       "er_bars_for_dead",        3),
        decaying_tolerance_bars = get("decaying_tolerance_bars","decaying_tolerance_bars", 1),

        # ── Regime ────────────────────────────────────────────────────────────
        regime_exhaustion_si_penalty  = get("regime_exhaustion_si_penalty",  default=0.10),
        regime_trending_with_si_bonus = get("regime_trending_with_si_bonus", default=0.05),
        trend_adx_thresh    = get("trend_adx_thresh",   "trend_adx_thresh",   65),
        exhaust_atr_thresh  = get("exhaust_atr_thresh",  "exhaust_atr_thresh",  75),
        exhaust_body_thresh = get("exhaust_body_thresh", "exhaust_body_thresh", 35),
        regime_bars         = get("regime_bars",         "regime_bars",         170),

        # ── SI Weights — tune per symbol (e.g. raise volume for XAUUSDm) ─────
        si_weight_cluster = get("si_weight_cluster", default=0.40),
        si_weight_regime  = get("si_weight_regime",  default=0.25),
        si_weight_adx     = get("si_weight_adx",     default=0.20),
        si_weight_volume  = get("si_weight_volume",  default=0.15),

        # ── Partial Close (v2.2) — CLI overrides config.json ─────────────────
        enable_partial_close          = enable_pc,
        si_partial_close_min          = get("si_partial_close_min",         default=args.partial_close_si),
        partial_close_profit_atr_mult = get("partial_close_profit_atr_mult",default=args.partial_close_atr),
        partial_close_fraction        = get("partial_close_fraction",        default=args.partial_close_frac),
    )


# ==============================================================================
#  BANNER
# ==============================================================================
def print_banner(symbols: list, args):
    print("=" * 64)
    print("  SuperTrend Bot v2.2 — Performance & Features Edition")
    print(f"  Symbols       : {', '.join(symbols)}")
    print(f"  Equity Filter : {'ON  (period=%d, ratio=%.2f)' % (args.equity_filter_period, args.equity_filter_ratio) if args.equity_filter else 'OFF'}")
    print(f"  Partial Close : {'ON  (SI>=%.2f, %.1f×ATR, %.0f%%)' % (args.partial_close_si, args.partial_close_atr, args.partial_close_frac*100) if args.partial_close else 'OFF'}")
    print(f"  Mode          : {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 64)


# ==============================================================================
#  MAIN
# ==============================================================================
def main():
    args   = parse_arguments()
    logger = setup_logging(args.log_level)

    # ── Resolve symbol list ────────────────────────────────────────────────────
    if args.symbols:
        symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    elif args.symbol:
        symbols = [args.symbol.strip()]
    else:
        symbols = ["EURUSDm"]
        logger.info("No symbol specified — defaulting to EURUSDm")

    print_banner(symbols, args)
    Path("logs").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    # ── Load JSON config ───────────────────────────────────────────────────────
    try:
        config_data = load_config(args.config)
        logger.info(f"Configuration loaded from {args.config}")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

    # ── Account credentials ────────────────────────────────────────────────────
    account_config = config_data["accounts"].get(args.account)
    if not account_config:
        logger.error(f"Account '{args.account}' not found in configuration")
        sys.exit(1)

    # ── Filter disabled symbols ────────────────────────────────────────────────
    valid_symbols = []
    for sym in symbols:
        sym_cfg = config_data.get("symbols", {}).get(sym, {})
        if not sym_cfg.get("enabled", True):
            logger.warning(f"Symbol '{sym}' is disabled in config — skipping")
            continue
        valid_symbols.append(sym)

    if not valid_symbols:
        logger.error("No valid/enabled symbols found — exiting")
        sys.exit(1)

    # ── Connect MT5 (once for all symbols) ────────────────────────────────────
    logger.info(f"Connecting to MT5 {args.account} account...")
    account_info = connect_mt5(
        account_config["login"],
        account_config["password"],
        account_config["server"],
        logger,
    )
    if account_info is None:
        sys.exit(1)

    logger.info(
        f"Connected | Account: {account_info.login} | "
        f"Balance: {account_info.balance} {account_info.currency} | "
        f"Leverage: 1:{account_info.leverage}"
    )

    # ── Build one Config + one SuperTrendBot per symbol ───────────────────────
    bots = []
    for sym in valid_symbols:
        cfg = build_config(sym, config_data, args)
        bot = SuperTrendBot(cfg)
        bot.is_connected = True
        bots.append(bot)
        logger.info(
            f"  [{sym}] TF={cfg.timeframe} | Risk={cfg.risk_percent}% | "
            f"MaxPos={cfg.max_positions} | "
            f"SL={cfg.sl_multiplier}×ATR | "
            f"Incubation: trend={cfg.incubation_bars_trending} "
            f"stable={cfg.incubation_bars_stable} "
            f"exhaust={cfg.incubation_bars_exhaustion} | "
            f"SI weights: C={cfg.si_weight_cluster} R={cfg.si_weight_regime} "
            f"A={cfg.si_weight_adx} V={cfg.si_weight_volume} | "
            f"PartialClose: {'ON' if cfg.enable_partial_close else 'OFF'}"
        )

    # ==========================================================================
    #  BACKTEST MODE
    # ==========================================================================
    if args.backtest:
        if len(bots) > 1:
            logger.warning(
                f"Backtest runs on first symbol only ({bots[0].config.symbol})"
            )
        from backtest_engine import BacktestEngine
        bot      = bots[0]
        engine   = BacktestEngine(strategy=bot, initial_balance=10000)
        end_dt   = datetime.now()
        start_dt = end_dt - timedelta(days=30)
        report   = engine.run_backtest(
            symbol=bot.config.symbol,
            start_date=start_dt,
            end_date=end_dt,
            timeframe=bot.config.timeframe,
        )
        print(report)
        mt5.shutdown()
        sys.exit(0)

    # ==========================================================================
    #  LIVE / DRY-RUN MODE
    # ==========================================================================
    if args.dry_run:
        logger.info("DRY RUN mode — no real trades will be placed")

    try:
        if len(bots) == 1:
            # Single-symbol legacy mode
            bot = bots[0]
            bot.dry_run = args.dry_run
            logger.info(
                f"Single-symbol mode | {bot.config.symbol} | "
                f"Interval: {args.interval}s"
            )
            bot.run(interval_seconds=args.interval)

        else:
            # Multi-pair mode with v2.2 runner features
            logger.info(
                f"Multi-pair mode | {[b.config.symbol for b in bots]} | "
                f"Interval: {args.interval}s | "
                f"GlobalCap: {args.max_total_positions}"
            )
            runner = MultiPairRunner(
                bots=bots,
                interval_seconds=args.interval,
                max_total_positions=args.max_total_positions,
                dry_run=args.dry_run,
                equity_filter_enabled=args.equity_filter,
                equity_filter_period=args.equity_filter_period,
                equity_filter_min_ratio=args.equity_filter_ratio,
            )
            runner.run()

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
    finally:
        mt5.shutdown()
        logger.info("MT5 connection closed")

        if args.monitor:
            logger.info("── Session Statistics ──")
            for bot in bots:
                stats = bot.calculate_statistics()
                logger.info(
                    f"  [{stats['symbol']}] "
                    f"Trades: {stats['total_trades']} | "
                    f"Win%: {stats.get('win_rate', 0)} | "
                    f"P&L: {stats.get('total_pnl', 0):.2f} | "
                    f"Cache: {stats.get('cache_hits', 0)} hits / "
                    f"{stats.get('cache_misses', 0)} misses"
                )

    logger.info("Bot shutdown complete")


if __name__ == "__main__":
    main()
