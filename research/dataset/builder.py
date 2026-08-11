from types import MappingProxyType
from research.store import FeatureStore, LabelStore
from research.dataset.result import Dataset, DatasetRecord
from research.dataset.errors import DatasetAlignmentError, DuplicateColumnError

def build_dataset(feature_store: FeatureStore, label_store: LabelStore) -> Dataset:
    """
    Structurally joins FeatureStore and LabelStore into an immutable Dataset.
    Performs NO mathematical operations, ML scaling, or missing-value imputation.
    """
    if len(feature_store) != len(label_store):
        raise DatasetAlignmentError(
            f"Store lengths do not match: FeatureStore ({len(feature_store)}) vs LabelStore ({len(label_store)})."
        )
        
    feature_seq = feature_store.get_all()
    label_seq = label_store.get_all()
    
    records = []
    global_feature_names = set()
    global_label_names = set()
    
    for i in range(len(feature_seq)):
        f_res = feature_seq[i]
        l_res = label_seq[i]
        
        if f_res.timestamp != l_res.timestamp:
            raise DatasetAlignmentError(
                f"Timestamp mismatch at index {i}: Feature ({f_res.timestamp}) vs Label ({l_res.timestamp})."
            )
            
        # Extract raw values from FeatureResult and LabelResult mappings
        features = {k: v.value for k, v in f_res.feature_results.items()}
        labels = {k: v.value for k, v in l_res.label_results.items()}
        
        # Check column collisions
        f_keys = set(features.keys())
        l_keys = set(labels.keys())
        
        collisions = f_keys.intersection(l_keys)
        if collisions:
            raise DuplicateColumnError(f"Duplicate column names detected across features and labels: {collisions}")
            
        global_feature_names.update(f_keys)
        global_label_names.update(l_keys)
        
        records.append(
            DatasetRecord(
                timestamp=f_res.timestamp,
                features=MappingProxyType(features),
                labels=MappingProxyType(labels)
            )
        )
        
    # Verify global namespace collisions across entire dataset
    global_collisions = global_feature_names.intersection(global_label_names)
    if global_collisions:
        raise DuplicateColumnError(f"Global duplicate column names detected: {global_collisions}")
        
    return Dataset(
        records=tuple(records),
        feature_names=frozenset(global_feature_names),
        label_names=frozenset(global_label_names)
    )
