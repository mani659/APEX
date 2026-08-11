"""
=========================================================
APEX Quant Research Framework

Module  : registry.py
Version : 3.0

Automatic Feature Registry

Author  : APEX
=========================================================
"""

import inspect
import importlib

# ==========================================================
# Registered Feature Modules
# ==========================================================

FEATURE_MODULES = {

    "price": "build_price_features",
    "volume": "build_volume_features",
    "volatility": "build_volatility_features",
    "trend": "build_trend_features",
    "momentum": "build_momentum_features",
    "structure": "build_structure_features",
    "smart_money": "build_smart_money_features",
    "regime": "build_regime_features",
    "session": "build_session_features",

}

FEATURE_REGISTRY = {}

# ==========================================================
# Build Registry
# ==========================================================

for module_name, function_name in FEATURE_MODULES.items():

    module = importlib.import_module(
        f"features.{module_name}"
    )

    if not hasattr(module, function_name):

        raise ImportError(

            f"{module_name}.py missing "

            f"'{function_name}'"

        )

    func = getattr(module, function_name)

    if not inspect.isfunction(func):

        raise TypeError(

            f"{function_name} "

            "is not a function."

        )

    FEATURE_REGISTRY[module_name] = func


# ==========================================================
# Public API
# ==========================================================

def get_registry():

    return FEATURE_REGISTRY


def list_modules():

    return list(FEATURE_REGISTRY.keys())


if __name__ == "__main__":

    print()

    print("Feature Registry")

    print("----------------")

    for name in FEATURE_REGISTRY:

        print(name)