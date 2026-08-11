"""
=========================================================
APEX Quant Research Framework

Module      : experiment_profiles.py
Version     : 1.0

=========================================================
"""

PROFILES = {

    "FAST": {

        "symbols": ["XAUUSD"],

        "save_dataset": False,

        "lookahead": 120,

    },

    "DEFAULT": {

        "symbols": ["XAUUSD"],

        "save_dataset": True,

        "lookahead": 240,

    },

    "MULTI_ASSET": {

        "symbols": [

            "XAUUSD",

            "XAGUSD",

            "BTCUSD",

            "EURUSD",

            "NAS100"

        ],

        "save_dataset": True,

        "lookahead": 240,

    }

}