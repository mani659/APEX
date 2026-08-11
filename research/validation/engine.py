from typing import List
from research.dataset.result import Dataset
from research.validation.report import ValidationReport, ValidationIssue, Severity
from research.validation.errors import DatasetValidationError

def validate(dataset: Dataset) -> ValidationReport:
    """
    Deterministically validates a dataset without mutating it.
    Checks for empty dataset, missing values, timestamp ordering, and duplicates.
    """
    issues: List[ValidationIssue] = []
    
    if dataset is None:
        raise DatasetValidationError("Engine failed: Provided dataset is None.")
        
    if not dataset.records:
        issues.append(ValidationIssue(
            severity=Severity.ERROR,
            category="Dataset Size",
            message="Dataset contains no records."
        ))
        return ValidationReport(
            valid=False,
            issue_count=1,
            error_count=1,
            warning_count=0,
            issues=tuple(issues)
        )
        
    expected_features = dataset.feature_names
    expected_labels = dataset.label_names
    
    prev_timestamp = None
    
    for i, record in enumerate(dataset.records):
        if not hasattr(record, 'timestamp') or record.timestamp is None:
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                category="Missing Timestamp",
                message=f"Record at index {i} is missing a timestamp.",
                record_index=i
            ))
            continue
            
        t = record.timestamp
        
        # 3. & 6. Timestamps strictly increasing (no duplicates, no out of order)
        if prev_timestamp is not None:
            if t == prev_timestamp:
                issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    category="Duplicate Timestamp",
                    message=f"Duplicate timestamp {t} at index {i}.",
                    record_index=i
                ))
            elif t < prev_timestamp:
                issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    category="Timestamp Ordering",
                    message=f"Timestamp {t} at index {i} is out of order (previous: {prev_timestamp}).",
                    record_index=i
                ))
        prev_timestamp = t
        
        # 4. Feature mappings are complete
        for f_name in expected_features:
            if f_name not in record.features:
                issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    category="Missing Feature",
                    message=f"Record missing expected feature '{f_name}'.",
                    record_index=i,
                    feature_name=f_name
                ))
            elif record.features[f_name] is None:
                 issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    category="Missing Feature Value",
                    message=f"Record has None for feature '{f_name}'.",
                    record_index=i,
                    feature_name=f_name
                ))

        # 5. Label mappings are complete
        for l_name in expected_labels:
            if l_name not in record.labels:
                issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    category="Missing Label",
                    message=f"Record missing expected label '{l_name}'.",
                    record_index=i,
                    label_name=l_name
                ))
            elif record.labels[l_name] is None:
                issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    category="Missing Label Value",
                    message=f"Record has None for label '{l_name}'.",
                    record_index=i,
                    label_name=l_name
                ))
                
    # 7. Dataset metadata exists
    if not hasattr(dataset, 'metadata') or dataset.metadata is None:
        issues.append(ValidationIssue(
            severity=Severity.ERROR,
            category="Missing Metadata",
            message="Dataset is missing metadata."
        ))
        
    error_count = sum(1 for iss in issues if iss.severity == Severity.ERROR)
    warning_count = sum(1 for iss in issues if iss.severity == Severity.WARNING)
    
    return ValidationReport(
        valid=(error_count == 0),
        issue_count=len(issues),
        error_count=error_count,
        warning_count=warning_count,
        issues=tuple(issues)
    )
