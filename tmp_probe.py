import importlib, sys
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
mods = ['features.price','features.volume','features.volatility','features.trend','features.momentum','features.structure','features.smart_money','features.regime','features.session','data.loader','data.validator','data.preprocessing','data.indicators','data.feature_builder','data.dataset_builder','labels.labels','labels.future_returns','labels.grid_labels','labels.survival_labels','labels.execution_labels','labels.validation']
for m in mods:
    try:
        importlib.import_module(m)
        print('OK', m)
    except Exception as e:
        print('FAIL', m, '=>', repr(e))
