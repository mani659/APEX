"""
=========================================================
APEX Doctor

Module : check_contracts.py
Version: 2.0

Verifies every feature module follows the
APEX Feature Contract.
=========================================================
"""

import inspect
import importlib
import pandas as pd

EXPECTED = {

    "price":"build_price_features",
    "volume":"build_volume_features",
    "volatility":"build_volatility_features",
    "trend":"build_trend_features",
    "momentum":"build_momentum_features",
    "structure":"build_structure_features",
    "smart_money":"build_smart_money_features",
    "regime":"build_regime_features",
    "session":"build_session_features",

}


def run_contract_check():

    print()
    print("="*60)
    print("FEATURE CONTRACT CHECK")
    print("="*60)

    ok = 0
    fail = 0

    sample = pd.DataFrame(
        {
            "open":[1,2,3],
            "high":[2,3,4],
            "low":[0,1,2],
            "close":[1.5,2.5,3.5],
            "volume":[100,110,90]
        }
    )

    for module_name,function_name in EXPECTED.items():

        try:

            module = importlib.import_module(
                f"features.{module_name}"
            )

            if not hasattr(module,function_name):

                raise Exception(
                    f"Missing {function_name}"
                )

            fn = getattr(module,function_name)

            sig = inspect.signature(fn)

            if len(sig.parameters)!=1:

                raise Exception(
                    "Expected one DataFrame argument"
                )

            out = fn(sample)

            if not isinstance(out,pd.DataFrame):

                raise Exception(
                    "Return type is not DataFrame"
                )

            print(f"[ OK ] {module_name}")

            ok += 1

        except Exception as e:

            print(f"[FAIL] {module_name}")

            print(f"       {e}")

            fail += 1

    print()

    print(f"Passed : {ok}")

    print(f"Failed : {fail}")