"""Factor changes and rolling betas. The beta on day t includes day t."""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategy_library.config import Factor
from strategy_library.factors.changes import build_factor_changes
from strategy_library.factors.regress import (
    comparison_book,
    hypothesis_status,
    rolling_ols,
    sign_flip_halves,
    sign_flip_windows,
)


def _reference_ols(y: np.ndarray, x: np.ndarray) -> tuple[float, float, float]:
    design = np.column_stack([np.ones(len(y)), x])
    slope = np.linalg.lstsq(design, y, rcond=None)[0]
    resid = y - design @ slope
    sse = float(np.sum(resid**2))
    sst = float(np.sum((y - y.mean()) ** 2))
    xtx = np.linalg.inv(design.T @ design)
    se = np.sqrt((sse / (len(y) - 2)) * xtx[1, 1])
    return float(slope[1]), float(slope[1] / se), 1.0 - sse / sst


def test_yield_slope_is_ten_minus_two_then_differenced() -> None:
    idx = pd.bdate_range("2020-01-01", periods=4)
    levels = {
        "USGG10YR Index": pd.Series([4.0, 4.2, 4.2, 4.5], index=idx),
        "USGG2YR Index": pd.Series([3.0, 3.0, 3.1, 3.1], index=idx),
    }
    factors = (
        Factor("us_10y", "10y", "diff", "percent", ticker="USGG10YR Index"),
        Factor("us_2y", "2y", "diff", "percent", ticker="USGG2YR Index"),
        Factor("us_2s10s", "slope", "diff", "percent", derived=("us_10y", "us_2y")),
    )
    changes = build_factor_changes(levels, factors)
    # Slope levels are 1.0, 1.2, 1.1, 1.4. Changes are the first difference, not a rescaling.
    assert list(changes["us_2s10s"].dropna().round(10)) == [0.2, -0.1, 0.3]
    assert list(changes["us_10y"].dropna().round(10)) == [0.2, 0.0, 0.3]


def test_percent_change_is_simple_not_log() -> None:
    idx = pd.bdate_range("2020-01-01", periods=3)
    levels = {"DXY Curncy": pd.Series([100.0, 110.0, 99.0], index=idx)}
    factors = (Factor("dxy", "dxy", "pct", "return", ticker="DXY Curncy"),)
    changes = build_factor_changes(levels, factors)
    assert abs(changes["dxy"].iloc[1] - 0.10) < 1e-12
    assert abs(changes["dxy"].iloc[2] - (99 / 110 - 1)) < 1e-12


def test_rolling_beta_matches_ols_and_includes_today() -> None:
    idx = pd.bdate_range("2020-01-01", periods=12)
    rng = np.random.default_rng(0)
    x = pd.Series(rng.normal(0, 0.01, len(idx)), index=idx)
    y = 2.0 * x + pd.Series(rng.normal(0, 0.001, len(idx)), index=idx)
    window = 8
    fit = rolling_ols(y, x, window)
    beta, tstat, r2 = _reference_ols(y.iloc[-window:].to_numpy(), x.iloc[-window:].to_numpy())
    assert abs(fit["beta"].iloc[-1] - beta) < 1e-8
    assert abs(fit["tstat"].iloc[-1] - tstat) < 1e-6
    assert abs(fit["r2"].iloc[-1] - r2) < 1e-8

    y_spike = y.copy()
    y_spike.iloc[-1] = 1.0
    spiked = rolling_ols(y_spike, x, window)
    # Yesterday's window does not contain today's spike. Today's window does.
    assert abs(spiked["beta"].iloc[-2] - fit["beta"].iloc[-2]) < 1e-12
    assert abs(spiked["beta"].iloc[-1] - fit["beta"].iloc[-1]) > 0.5


def test_sign_flags_and_hypothesis() -> None:
    idx = pd.bdate_range("2020-01-01", periods=6)
    short = pd.Series([0.2, 0.2, 0.2, 0.2, 0.2, -0.4], index=idx)
    long = pd.Series([0.3, 0.3, 0.3, 0.3, 0.3, 0.3], index=idx)
    assert sign_flip_windows(short, long)
    halves = pd.Series([1.0, 1.0, 1.0, -1.0, -1.0, -1.0], index=idx)
    assert sign_flip_halves(halves)
    assert not sign_flip_halves(pd.Series([1.0, 0.5, 0.2, 0.2], index=idx[:4]))
    assert hypothesis_status(0.2, "+") == "matches"
    assert hypothesis_status(-0.2, "+") == "disagrees"
    assert hypothesis_status(np.nan, "-") == "no_estimate"
    assert comparison_book("JPY") == "local"
    assert comparison_book("mixed") == "usd"
