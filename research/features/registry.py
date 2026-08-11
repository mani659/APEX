from typing import Dict, List
from research.features.base import Feature

class FeatureRegistry:
    """
    Simple static registry for research features.
    No dynamic reflection or plugin loading.
    """
    def __init__(self):
        self._registry: Dict[str, Feature] = {}
        
    def register(self, feature: Feature):
        if feature.name in self._registry:
            raise ValueError(f"Feature with name '{feature.name}' is already registered.")
        self._registry[feature.name] = feature
        
    def get(self, name: str) -> Feature:
        if name not in self._registry:
            raise KeyError(f"Feature '{name}' not found in registry.")
        return self._registry[name]
        
    def list_features(self) -> List[str]:
        return list(self._registry.keys())
