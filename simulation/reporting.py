from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Dict, Any, List, Optional, Tuple

from simulation.statistics import StatisticsSummary
from simulation.portfolio import PortfolioSnapshot
# These imports assume the respective modules have these result dataclasses defined.
# If they don't exactly match, the architecture rule is just to consume them via public DTOs.
from simulation.walkforward import WalkForwardResult
from simulation.montecarlo import MonteCarloResult
from simulation.optimization import OptimizationResult
from simulation.experiment import ExperimentRecord, ExperimentComparison

@dataclass(frozen=True)
class ReportConfig:
    report_title: str = "Research Report"
    author: str = "APEX Framework"
    organization: str = "Quantitative Research"
    include_summary: bool = True
    include_equity_curve: bool = True
    include_drawdown_curve: bool = True
    include_statistics: bool = True
    include_trade_distribution: bool = True
    include_monte_carlo: bool = True
    include_walk_forward: bool = True
    include_optimization: bool = True
    include_experiment_metadata: bool = True
    theme: str = "light"
    output_format: str = "markdown" # "markdown" or "html"
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

@dataclass(frozen=True)
class ReportSection:
    title: str
    content: str
    order: int
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

@dataclass(frozen=True)
class ReportDocument:
    title: str
    generated_timestamp: datetime
    configuration: ReportConfig
    sections: Tuple[ReportSection, ...]
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

class ReportGenerator:
    """
    Pure presentation layer. Generates reports from immutable outputs produced by the research framework.
    Performs zero financial calculations, simulations, or optimizations.
    """
    
    def generate(
        self,
        config: ReportConfig,
        stats: Optional[StatisticsSummary] = None,
        snapshots: Optional[List[PortfolioSnapshot]] = None,
        wf_result: Optional[WalkForwardResult] = None,
        mc_result: Optional[MonteCarloResult] = None,
        opt_result: Optional[OptimizationResult] = None,
        experiment_record: Optional[ExperimentRecord] = None,
        experiment_comparison: Optional[ExperimentComparison] = None
    ) -> str:
        
        sections: List[ReportSection] = []
        order = 0
        
        if config.include_summary:
            order += 1
            sections.append(ReportSection(
                title="Executive Summary",
                content=self._build_summary(config),
                order=order
            ))
            
        if config.include_experiment_metadata and experiment_record:
            order += 1
            sections.append(ReportSection(
                title="Experiment Metadata",
                content=self._build_experiment_metadata(experiment_record),
                order=order
            ))
            
        if config.include_statistics and stats:
            order += 1
            sections.append(ReportSection(
                title="Performance Statistics",
                content=self._build_statistics(stats),
                order=order
            ))
            
        if (config.include_equity_curve or config.include_drawdown_curve) and snapshots:
            order += 1
            sections.append(ReportSection(
                title="Portfolio Summary",
                content=self._build_portfolio_summary(snapshots, config),
                order=order
            ))
            
        if config.include_optimization and opt_result:
            order += 1
            sections.append(ReportSection(
                title="Optimization Summary",
                content=self._build_optimization(opt_result),
                order=order
            ))
            
        if config.include_walk_forward and wf_result:
            order += 1
            sections.append(ReportSection(
                title="Walk-Forward Summary",
                content=self._build_walk_forward(wf_result),
                order=order
            ))
            
        if config.include_monte_carlo and mc_result:
            order += 1
            sections.append(ReportSection(
                title="Monte Carlo Summary",
                content=self._build_monte_carlo(mc_result),
                order=order
            ))
            
        if experiment_comparison:
            order += 1
            sections.append(ReportSection(
                title="Experiment Comparison",
                content=self._build_comparison(experiment_comparison),
                order=order
            ))
            
        document = ReportDocument(
            title=config.report_title,
            generated_timestamp=datetime.now(timezone.utc),
            configuration=config,
            sections=tuple(sections)
        )
        
        if config.output_format.lower() == "html":
            return self._format_html(document)
        else:
            return self._format_markdown(document)
            
    def _build_summary(self, config: ReportConfig) -> str:
        return f"This report was generated by the APEX Framework for {config.organization} by {config.author}."
        
    def _build_experiment_metadata(self, record: ExperimentRecord) -> str:
        lines = [
            f"- **Experiment ID:** {record.experiment_id}",
            f"- **Started:** {record.timestamp_started.isoformat()}",
            f"- **Duration:** {record.duration_seconds:.2f} seconds",
            f"- **Research Mode:** {record.research_component_used.name}"
        ]
        return "\n".join(lines)
        
    def _build_statistics(self, stats: StatisticsSummary) -> str:
        lines = [
            f"- **Total Trades:** {stats.total_trades}",
            f"- **Net Profit:** {stats.net_profit:.2f}",
            f"- **Profit Factor:** {stats.profit_factor:.2f}",
            f"- **Win Rate:** {stats.win_rate:.2%}",
            f"- **Max Drawdown:** {stats.maximum_drawdown:.2f}",
            f"- **Expectancy:** {stats.expectancy:.2f}"
        ]
        return "\n".join(lines)
        
    def _build_portfolio_summary(self, snapshots: List[PortfolioSnapshot], config: ReportConfig) -> str:
        if not snapshots:
            return "No portfolio data provided."
        first = snapshots[0]
        last = snapshots[-1]
        lines = [
            f"- **Initial Equity:** {first.equity:.2f}",
            f"- **Final Equity:** {last.equity:.2f}",
            f"- **Total Snapshots:** {len(snapshots)}"
        ]
        if config.include_equity_curve:
            lines.append("\n*(Text-based equity rendering omitted, please refer to analytics dashboard)*")
        return "\n".join(lines)
        
    def _build_optimization(self, result: OptimizationResult) -> str:
        lines = [
            f"- **Evaluations:** {result.number_of_evaluations}",
            f"- **Best Objective Value:** {result.objective_value:.2f}",
            f"- **Best Parameters:**"
        ]
        for k, v in result.best_parameters.items():
            lines.append(f"  - `{k}`: {v}")
        return "\n".join(lines)
        
    def _build_walk_forward(self, result: WalkForwardResult) -> str:
        lines = [
            f"- **Total Windows:** {len(result.windows)}",
            f"- **Robustness Ratio:** {result.stability_metrics.get('robustness_ratio', 0.0):.2f}",
            f"- **Overall Pass:** {'Yes' if result.overall_pass else 'No'}",
            f"- **Aggregate Net Profit:** {result.aggregate_statistics.get('net_profit', 0.0):.2f}"
        ]
        return "\n".join(lines)
        
    def _build_monte_carlo(self, result: MonteCarloResult) -> str:
        net_p50 = result.aggregates.get('net_profit', {}).get('p50', 0.0)
        dd_p99 = result.aggregates.get('maximum_drawdown', {}).get('p99', 0.0)
        lines = [
            f"- **Total Runs:** {result.number_of_runs}",
            f"- **Median Profit:** {net_p50:.2f}",
            f"- **Worst Max Drawdown (99th):** {dd_p99:.2f}",
            f"- **Risk of Ruin (Positive Profit Prob):** {result.prob_net_profit_positive:.2%}"
        ]
        return "\n".join(lines)
        
    def _build_comparison(self, comp: ExperimentComparison) -> str:
        lines = [
            f"- **Winner:** {comp.winner.capitalize()}",
            f"- **Baseline ID:** {comp.baseline_experiment.experiment_id}",
            f"- **Candidate ID:** {comp.candidate_experiment.experiment_id}",
            "",
            "**Metric Differences (Candidate - Baseline):**"
        ]
        for k, v in comp.metric_differences.items():
            lines.append(f"- `{k}`: {v:+.2f}")
        return "\n".join(lines)
        
    def _format_markdown(self, document: ReportDocument) -> str:
        lines = [
            f"# {document.title}",
            f"**Generated:** {document.generated_timestamp.isoformat()}",
            "---",
            ""
        ]
        
        for section in sorted(document.sections, key=lambda s: s.order):
            lines.append(f"## {section.title}")
            lines.append(section.content)
            lines.append("")
            
        return "\n".join(lines).strip()
        
    def _format_html(self, document: ReportDocument) -> str:
        html = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            f"<title>{document.title}</title>",
            "<style>",
            "body { font-family: sans-serif; max-width: 800px; margin: auto; padding: 20px; }",
            "h1 { border-bottom: 2px solid #ccc; }",
            "h2 { color: #333; margin-top: 30px; }",
            "ul { line-height: 1.6; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{document.title}</h1>",
            f"<p><strong>Generated:</strong> {document.generated_timestamp.isoformat()}</p>",
            "<hr/>"
        ]
        
        for section in sorted(document.sections, key=lambda s: s.order):
            html.append(f"<h2>{section.title}</h2>")
            # Extremely basic markdown-to-html list conversion for our controlled text
            content_html = section.content.replace("\n", "<br/>")
            # Replace list items roughly
            content_html = content_html.replace("- **", "<li><strong>").replace(":**", ":</strong>")
            html.append(f"<p>{content_html}</p>")
            
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)
