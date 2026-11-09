"""Desk-facing HTML and markdown reports. No Bloomberg imports."""

from strategy_library.reports.factor_map import build_factor_map_payload, render_factor_map_html

__all__ = ["build_factor_map_payload", "render_factor_map_html"]
