"""
=========================================================
APEX Quant Research Framework

Module      : campaign_runner.py
Version     : 1.0

Description :
Abstract base class and runner for Research Campaigns.
Consumes analytics outputs and generates markdown reports.
=========================================================
"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict


class Campaign(ABC):
    """
    Abstract base class for all APEX research campaigns.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Campaign identifier (e.g. 'RC001_Continuation')."""
        pass

    @property
    @abstractmethod
    def research_question(self) -> str:
        """The scientific question being asked."""
        pass

    @property
    @abstractmethod
    def hypothesis(self) -> str:
        """The testable hypothesis."""
        pass

    @property
    @abstractmethod
    def required_analytics(self) -> List[str]:
        """List of required analytics directories (e.g. ['statistics', 'regimes'])."""
        pass

    @abstractmethod
    def execute(self, analytics_dir: Path) -> Dict[str, str]:
        """
        Executes the campaign logic.
        Returns:
            Dict[str, str]: Dictionary mapping filenames (e.g. 'Findings.md') to markdown content.
        """
        pass


def run_campaign(campaign: Campaign, analytics_dir: Path, output_base_dir: Path) -> None:
    """
    Orchestrates the campaign execution.
    """
    print("=" * 60)
    print("APEX RESEARCH CAMPAIGN RUNNER")
    print("=" * 60)
    print(f"Campaign : {campaign.name}")
    print(f"Analytics: {analytics_dir}")

    if not analytics_dir.exists():
        raise FileNotFoundError(f"Analytics directory not found: {analytics_dir}")

    # Validate requirements
    for req in campaign.required_analytics:
        req_path = analytics_dir / req
        if not req_path.exists():
            raise FileNotFoundError(
                f"Required analytics artifact '{req}' missing from {analytics_dir}."
            )

    print("Status   : Running...")

    try:
        output_files = campaign.execute(analytics_dir)
    except Exception as e:
        print(f"ERROR    : Campaign failed to execute.\n{e}")
        raise

    campaign_dir = output_base_dir / campaign.name
    campaign_dir.mkdir(parents=True, exist_ok=True)

    # Write Research Question
    question_content = (
        f"# {campaign.name}\n\n"
        f"## Research Question\n{campaign.research_question}\n\n"
        f"## Hypothesis\n{campaign.hypothesis}\n"
    )
    (campaign_dir / "Research_Question.md").write_text(question_content, encoding="utf-8")

    # Write dynamic outputs
    for filename, content in output_files.items():
        (campaign_dir / filename).write_text(content, encoding="utf-8")

    # Write Metadata
    metadata = {
        "campaign_name": campaign.name,
        "research_question": campaign.research_question,
        "hypothesis": campaign.hypothesis,
        "timestamp": datetime.now().isoformat(),
        "analytics_source": str(analytics_dir)
    }
    with open(campaign_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print("Status   : Complete")
    print(f"Output   : {campaign_dir}")
    print("=" * 60)
