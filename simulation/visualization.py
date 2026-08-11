import math
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import List, Dict, Any, Optional

from simulation.portfolio import PortfolioSnapshot
from simulation.montecarlo import MonteCarloResult

@dataclass(frozen=True)
class VisualizationConfig:
    width: int = 800
    height: int = 400
    theme: str = "dark" # "dark" or "light"
    format: str = "svg" # "svg" or "html" (png not natively supported without libs)
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

@dataclass(frozen=True)
class ChartDefinition:
    title: str
    chart_type: str
    x_label: str
    y_label: str

@dataclass(frozen=True)
class ChartResult:
    definition: ChartDefinition
    format: str
    data: bytes
    metadata: MappingProxyType = field(default_factory=lambda: MappingProxyType({}))

class VisualizationEngine:
    """
    Renders purely native, library-free SVG / HTML visualizations from immutable DTOs.
    Performs ZERO calculations and ZERO simulation.
    """
    
    def visualize_equity_curve(self, snapshots: List[PortfolioSnapshot], config: VisualizationConfig) -> ChartResult:
        if not snapshots:
            return self._empty_chart("Equity Curve", config)
            
        points = [(i, float(s.equity)) for i, s in enumerate(snapshots)]
        data = self._render_line_chart(points, "Equity Curve", "Time", "Equity", config)
        
        return ChartResult(
            definition=ChartDefinition("Equity Curve", "line", "Time", "Equity"),
            format=config.format,
            data=data.encode('utf-8')
        )
        
    def visualize_drawdown_curve(self, snapshots: List[PortfolioSnapshot], config: VisualizationConfig) -> ChartResult:
        if not snapshots:
            return self._empty_chart("Drawdown Curve", config)
            
        points = [(i, float(s.drawdown)) for i, s in enumerate(snapshots)]
        data = self._render_line_chart(points, "Drawdown Curve", "Time", "Drawdown", config)
        
        return ChartResult(
            definition=ChartDefinition("Drawdown Curve", "line", "Time", "Drawdown"),
            format=config.format,
            data=data.encode('utf-8')
        )

    def visualize_monte_carlo_distribution(self, result: MonteCarloResult, config: VisualizationConfig) -> ChartResult:
        if not result.net_profit_distribution:
            return self._empty_chart("Monte Carlo Net Profit Distribution", config)
            
        data = self._render_histogram(result.net_profit_distribution, "Monte Carlo Net Profit Distribution", "Net Profit", "Frequency", config)
        
        return ChartResult(
            definition=ChartDefinition("Monte Carlo Net Profit Distribution", "histogram", "Net Profit", "Frequency"),
            format=config.format,
            data=data.encode('utf-8')
        )
        
    def _empty_chart(self, title: str, config: VisualizationConfig) -> ChartResult:
        data = f'<svg width="{config.width}" height="{config.height}" xmlns="http://www.w3.org/2000/svg"><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle">No data for {title}</text></svg>'
        if config.format == "html":
            data = f"<div>{data}</div>"
        return ChartResult(
            definition=ChartDefinition(title, "empty", "", ""),
            format=config.format,
            data=data.encode('utf-8')
        )

    def _render_line_chart(self, points: List[tuple], title: str, xlabel: str, ylabel: str, config: VisualizationConfig) -> str:
        if not points:
            return ""
            
        bg_color = "#1e1e1e" if config.theme == "dark" else "#ffffff"
        text_color = "#ffffff" if config.theme == "dark" else "#000000"
        line_color = "#00ff00"
        
        pad_x = 50
        pad_y = 50
        
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        range_x = (max_x - min_x) if (max_x - min_x) > 0 else 1
        range_y = (max_y - min_y) if (max_y - min_y) > 0 else 1
        
        svg_pts = []
        for x, y in points:
            px = pad_x + ((x - min_x) / range_x) * (config.width - 2 * pad_x)
            py = config.height - pad_y - ((y - min_y) / range_y) * (config.height - 2 * pad_y)
            svg_pts.append(f"{px},{py}")
            
        path_d = "M " + " L ".join(svg_pts)
        
        svg = (
            f'<svg width="{config.width}" height="{config.height}" xmlns="http://www.w3.org/2000/svg">\n'
            f'  <rect width="100%" height="100%" fill="{bg_color}" />\n'
            f'  <text x="{config.width/2}" y="30" fill="{text_color}" text-anchor="middle" font-family="sans-serif" font-size="16">{title}</text>\n'
            f'  <path d="{path_d}" fill="none" stroke="{line_color}" stroke-width="2" />\n'
            f'</svg>'
        )
        
        if config.format == "html":
            return f"<div>{svg}</div>"
        return svg

    def _render_histogram(self, values: List[float], title: str, xlabel: str, ylabel: str, config: VisualizationConfig) -> str:
        if not values:
            return ""
            
        bg_color = "#1e1e1e" if config.theme == "dark" else "#ffffff"
        text_color = "#ffffff" if config.theme == "dark" else "#000000"
        bar_color = "#3498db"
        
        bins = 20
        min_v, max_v = min(values), max(values)
        range_v = max_v - min_v if max_v > min_v else 1
        bin_width = range_v / bins
        
        histogram = [0] * bins
        for v in values:
            b = int((v - min_v) / bin_width)
            if b == bins:
                b -= 1
            histogram[b] += 1
            
        pad_x = 50
        pad_y = 50
        max_h = max(histogram) if histogram else 1
        
        chart_w = config.width - 2 * pad_x
        chart_h = config.height - 2 * pad_y
        bar_w = chart_w / bins
        
        rects = []
        for i, count in enumerate(histogram):
            h = (count / max_h) * chart_h
            x = pad_x + i * bar_w
            y = config.height - pad_y - h
            rects.append(f'<rect x="{x}" y="{y}" width="{max(1, bar_w - 2)}" height="{h}" fill="{bar_color}" />')
            
        svg = (
            f'<svg width="{config.width}" height="{config.height}" xmlns="http://www.w3.org/2000/svg">\n'
            f'  <rect width="100%" height="100%" fill="{bg_color}" />\n'
            f'  <text x="{config.width/2}" y="30" fill="{text_color}" text-anchor="middle" font-family="sans-serif" font-size="16">{title}</text>\n'
            f'  {"".join(rects)}\n'
            f'</svg>'
        )
        
        if config.format == "html":
            return f"<div>{svg}</div>"
        return svg
