"""
=========================================================
APEX Quant Research Framework

Module      : validation.py
Version     : 2.0

Description :
Research Validation Framework.
The official scientific referee of APEX.
Evaluates objective evidence to determine classification.
=========================================================
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Any


@dataclass
class ValidationResult:
    campaign: str
    classification: str
    score: int
    criteria: Dict[str, int]
    passed: List[str]
    failed: List[str]
    recommendations: List[str]
    timestamp: str


def validate_campaign(campaign_name: str, evidence: dict) -> ValidationResult:
    """
    Validates a research campaign purely based on objective evidence.
    No subjective judgement.
    """
    
    # 1. Evaluate Criteria
    criteria = {}
    passed = []
    failed = []
    recommendations = []
    
    # Extract evidence safely
    sample_size = evidence.get("sample_size", 0)
    is_consistent = evidence.get("is_consistent", False)
    is_temporally_stable = evidence.get("is_temporally_stable", False)
    is_regime_stable = evidence.get("is_regime_stable", False)
    has_tail_risk = evidence.get("has_tail_risk", True) # Default conservative
    data_quality_ok = evidence.get("data_quality_ok", False)
    
    # Sample Size
    if sample_size >= 500:
        criteria["Sample Size"] = 1
        passed.append("Sample Size: Sufficient observations.")
    else:
        criteria["Sample Size"] = 0
        failed.append(f"Sample Size: Insufficient observations ({sample_size}).")
        recommendations.append("Increase dataset timeframe to achieve statistical significance.")
        
    # Consistency
    if is_consistent:
        criteria["Consistency"] = 1
        passed.append("Consistency: Effect direction remains consistent.")
    else:
        criteria["Consistency"] = 0
        failed.append("Consistency: Effect direction is weak or inconsistent.")
        recommendations.append("Isolate specific regimes where the edge is stronger.")
        
    # Temporal Stability
    if is_temporally_stable:
        criteria["Temporal Stability"] = 1
        passed.append("Temporal Stability: Acceptable variation through time.")
    else:
        criteria["Temporal Stability"] = 0
        failed.append("Temporal Stability: High variance or deterioration detected.")
        recommendations.append("Conduct ablation studies to identify periods of failure.")
        
    # Regime Stability
    if is_regime_stable:
        criteria["Regime Stability"] = 1
        passed.append("Regime Stability: Not concentrated in one isolated regime.")
    else:
        criteria["Regime Stability"] = 0
        failed.append("Regime Stability: Edge is too concentrated or fails in baseline regimes.")
        
    # Tail Risk
    if not has_tail_risk:
        criteria["Tail Risk"] = 1
        passed.append("Tail Risk: No severe instability indicated by analytics.")
    else:
        criteria["Tail Risk"] = 0
        failed.append("Tail Risk: Severe drawdowns or heavy tails detected.")
        recommendations.append("Implement aggressive position sizing or filters.")
        
    # Data Quality
    if data_quality_ok:
        criteria["Data Quality"] = 1
        passed.append("Data Quality: Analytics completed successfully.")
    else:
        criteria["Data Quality"] = 0
        failed.append("Data Quality: Missing or corrupted analytics artifacts.")
        recommendations.append("Resolve missing analytics dependencies before proceeding.")
        
    # 2. Compute Score
    total_criteria = len(criteria)
    points_earned = sum(criteria.values())
    score = int((points_earned / total_criteria) * 100) if total_criteria > 0 else 0
    
    # 3. Determine Classification
    classification = "REJECTED"
    
    # Critical criteria: Sample Size, Data Quality must pass for SUPPORTED
    critical_pass = criteria.get("Sample Size", 0) == 1 and criteria.get("Data Quality", 0) == 1
    
    if score >= 80 and critical_pass:
        classification = "SUPPORTED"
    elif score >= 50:
        classification = "PARTIALLY_SUPPORTED"
    else:
        classification = "REJECTED"
        
    if classification == "REJECTED" and "Reject hypothesis and reformulate feature logic." not in recommendations:
        recommendations.append("Reject hypothesis and reformulate feature logic.")
        
    if classification == "SUPPORTED" and "Proceed to walk-forward simulation." not in recommendations:
        recommendations.append("Proceed to walk-forward simulation.")
        
    return ValidationResult(
        campaign=campaign_name,
        classification=classification,
        score=score,
        criteria=criteria,
        passed=passed,
        failed=failed,
        recommendations=recommendations,
        timestamp=datetime.now().isoformat()
    )


def generate_validation_report(result: ValidationResult) -> str:
    """Helper to format the ValidationResult into a markdown report."""
    md = [
        "# APEX Research Validation Report\n",
        f"**Campaign**: {result.campaign}",
        f"**Classification**: {result.classification}",
        f"**Score**: {result.score}/100",
        f"**Timestamp**: {result.timestamp}\n",
        "## Passed Criteria\n"
    ]
    
    if result.passed:
        for p in result.passed:
            md.append(f"- [PASS] {p}")
    else:
        md.append("- None")
        
    md.append("\n## Failed Criteria\n")
    if result.failed:
        for f in result.failed:
            md.append(f"- [FAIL] {f}")
    else:
        md.append("- None")
        
    md.append("\n## Recommendations\n")
    if result.recommendations:
        for r in result.recommendations:
            md.append(f"- {r}")
    else:
        md.append("- None")
        
    return "\n".join(md)

def generate_conclusion_md(result: ValidationResult) -> str:
    """Helper to format a standard Conclusion.md."""
    md = [
        f"# Conclusion: {result.campaign}\n",
        f"Based on objective, data-driven validation, this hypothesis is officially classified as **{result.classification}**.\n",
        f"The campaign achieved a validation score of **{result.score}/100**.\n",
        "## Next Steps"
    ]
    for r in result.recommendations:
        md.append(f"- {r}")
        
    return "\n".join(md)
