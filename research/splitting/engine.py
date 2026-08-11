from research.dataset.result import Dataset
from research.splitting.config import SplitConfig
from research.splitting.result import DatasetSplit
from research.splitting.errors import SplitError

def split(dataset: Dataset, config: SplitConfig) -> DatasetSplit:
    """
    Deterministically partitions a dataset into train, validation, and test sets.
    Preserves chronological ordering. Never mutates the original dataset.
    """
    if dataset is None:
        raise SplitError("Dataset cannot be None.")
        
    if config is None:
        raise SplitError("SplitConfig cannot be None.")
        
    total_len = len(dataset.records)
    
    # Calculate deterministic split indices
    train_end = int(total_len * config.train_ratio)
    val_end = train_end + int(total_len * config.validation_ratio)
    
    # Create deterministic slices
    train_records = dataset.records[:train_end]
    val_records = dataset.records[train_end:val_end]
    test_records = dataset.records[val_end:]
    
    # Construct immutable sub-datasets
    train_dataset = Dataset(
        records=train_records,
        feature_names=dataset.feature_names,
        label_names=dataset.label_names,
        metadata=dataset.metadata
    )
    
    val_dataset = Dataset(
        records=val_records,
        feature_names=dataset.feature_names,
        label_names=dataset.label_names,
        metadata=dataset.metadata
    )
    
    test_dataset = Dataset(
        records=test_records,
        feature_names=dataset.feature_names,
        label_names=dataset.label_names,
        metadata=dataset.metadata
    )
    
    return DatasetSplit(
        train_dataset=train_dataset,
        validation_dataset=val_dataset,
        test_dataset=test_dataset,
        configuration=config
    )
