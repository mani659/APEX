"""
=========================================================
APEX Quant Research Framework
Module      : analytics
Description : Analytics and research evidence generation package.
=========================================================
"""

from analytics.analytics import run_analytics
from analytics.feature_importance import analyze as analyze_importance
from analytics.parameter_surface import analyze as analyze_surface
from analytics.reporting import analyze as analyze_reporting
from analytics.statistics import analyze as analyze_statistics
from analytics.tail_statistics import analyze as analyze_tails
from analytics.utils import AnalyticsResult

__all__ = [
    "AnalyticsResult",
    "run_analytics",
    "analyze_statistics",
    "analyze_tails",
    "analyze_importance",
    "analyze_surface",
    "analyze_reporting",
]
