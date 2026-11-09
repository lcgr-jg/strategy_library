"""Factor map payload stays small and scales yields the desk way."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from strategy_library.config import Factor, Leg, Spread
from strategy_library.reports.factor_map import (
    FactorMapPaths,
    build_factor_map_payload,
    effect_scale,
    render_factor_map_html,
    weekly_points,
)


def test_weekly_points_keep_last_print_of_each_week() -> None:
    idx = pd.to_datetime(["2020-01-06", "2020-01-07", "2020-01-13", "2020-01-14"])
    series = pd.Series([1.0, 2.0, 3.0, 4.0], index=idx)
    dates, values = weekly_points(series)
    assert dates == ["2020-01-07", "2020-01-14"]
    assert values == [2.0, 4.0]


def test_yield_scale_is_ten_for_ten_bp() -> None:
    assert effect_scale("yield") == 10.0
    assert effect_scale("price") == 1.0


def test_payload_and_html_from_tiny_cache(tmp_path: Path) -> None:
    sized_dir = tmp_path / "sized"
    beta_dir = tmp_path / "betas"
    sized_dir.mkdir()
    beta_dir.mkdir()
    idx = pd.bdate_range("2020-01-01", periods=12)
    sized = pd.DataFrame(
        {
            "idx_beta_local": range(100, 112),
            "basis_flag": [""] * 12,
        },
        index=idx,
    )
    sized.to_parquet(sized_dir / "demo.parquet")
    beta = pd.DataFrame(
        {
            "beta|local|us_10y|63|beta": [0.1] * 12,
            "beta|local|us_10y|63|tstat": [2.5] * 12,
            "beta|local|us_10y|252|beta": [0.2] * 12,
            "beta|local|us_10y|252|tstat": [3.0] * 12,
        },
        index=idx,
    )
    beta.to_parquet(beta_dir / "demo.parquet")
    latest = pd.DataFrame(
        [
            {
                "spread": "demo",
                "sizing": "beta",
                "book": "local",
                "is_comparison_book": True,
                "factor": "us_10y",
                "window": 63,
                "beta": 0.1,
                "tstat": 2.5,
                "r2": 0.1,
                "sign_flip_windows": False,
                "sign_flip_halves": False,
                "notable_window_flip": False,
                "basis_flag": "",
                "factor_timing": "same_calendar_date",
            },
            {
                "spread": "demo",
                "sizing": "beta",
                "book": "local",
                "is_comparison_book": True,
                "factor": "us_10y",
                "window": 252,
                "beta": 0.2,
                "tstat": 3.0,
                "r2": 0.1,
                "sign_flip_windows": False,
                "sign_flip_halves": False,
                "notable_window_flip": False,
                "basis_flag": "",
                "factor_timing": "same_calendar_date",
            },
        ]
    )
    latest_csv = tmp_path / "latest.csv"
    latest.to_csv(latest_csv, index=False)
    spreads = (
        Spread(
            id="demo",
            name="Demo vs Demo",
            long=(Leg(ticker="A Index", currency="USD", region="US"),),
            short=(Leg(ticker="B Index", currency="USD", region="US"),),
            region="US",
            currency="USD",
            themes=(),
            expected_drivers={"us_10y": "+"},
            sizing_default="beta_neutral",
            vol_long=None,
            vol_short=None,
            alignment="native",
        ),
    )
    factors = (Factor("us_10y", "US 10y", "diff", "percent", ticker="USGG10YR Index"),)
    payload = build_factor_map_payload(
        spreads,
        factors,
        FactorMapPaths(sized_dir=sized_dir, beta_dir=beta_dir, latest_csv=latest_csv),
        short_window=63,
        long_window=252,
    )
    assert payload["latest"][0]["lb"] == 0.2
    assert payload["performance"]["demo"]["values"]
    assert payload["betas"]["demo"]["us_10y"]["w252"]["values"]
    html = render_factor_map_html(payload)
    assert "Spread factor map" in html
    assert "plotly" in html.lower()
    assert "demo" in html
