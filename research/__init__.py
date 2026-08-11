"""
=========================================================
APEX Quant Research Framework
Research Package
=========================================================
"""

from research.campaign_runner import Campaign, run_campaign
from research.continuation import ContinuationCampaign
from research.continuation_expectancy import ContinuationExpectancyCampaign
from research.temporal_stability import TemporalStabilityCampaign
from research.execution_robustness import ExecutionRobustnessCampaign

__all__ = [
    "Campaign",
    "run_campaign",
    "ContinuationCampaign",
    "ContinuationExpectancyCampaign",
    "TemporalStabilityCampaign",
    "ExecutionRobustnessCampaign"
]
