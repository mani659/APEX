import statistics
from datetime import datetime
from research.dataset.result import Dataset
from research.analysis.result import FeatureAnalysisResult, FeatureMetrics
from research.analysis.errors import FeatureAnalysisError

def analyze(dataset: Dataset) -> FeatureAnalysisResult:
    """
    Analyzes the statistical quality of features in a dataset.
    Returns immutable analysis results.
    """
    if dataset is None:
        raise FeatureAnalysisError("Dataset is None.")
        
    total_records = len(dataset.records)
    if total_records == 0:
        raise FeatureAnalysisError("Dataset is empty.")
        
    metrics_list = []
    
    # Sort feature names for deterministic ordering
    feature_names = sorted(list(dataset.feature_names))
    
    for f_name in feature_names:
        values = []
        missing_count = 0
        
        for record in dataset.records:
            if f_name not in record.features or record.features[f_name] is None:
                missing_count += 1
            else:
                values.append(record.features[f_name])
                
        sample_count = len(values)
        missing_ratio = missing_count / total_records if total_records > 0 else 0.0
        
        if sample_count > 0:
            f_min = min(values)
            f_max = max(values)
            f_mean = statistics.mean(values)
            f_median = statistics.median(values)
        else:
            f_min = 0.0
            f_max = 0.0
            f_mean = 0.0
            f_median = 0.0
            
        if sample_count > 1:
            f_variance = statistics.variance(values)
            f_stdev = statistics.stdev(values)
        else:
            f_variance = 0.0
            f_stdev = 0.0
            
        metrics = FeatureMetrics(
            feature_name=f_name,
            sample_count=sample_count,
            mean=float(f_mean),
            median=float(f_median),
            minimum=float(f_min),
            maximum=float(f_max),
            variance=float(f_variance),
            standard_deviation=float(f_stdev),
            missing_ratio=float(missing_ratio)
        )
        metrics_list.append(metrics)
        
    return FeatureAnalysisResult(
        feature_count=len(feature_names),
        analyzed_timestamp=datetime.now().isoformat(),
        feature_metrics=tuple(metrics_list)
    )
