"""Sizing uses lagged windows. A spike today cannot change today's hedge."""

from __future__ import annotations

import pandas as pd

from strategy_library.config import Settings
from strategy_library.data.basis import net_vs_gross
from strategy_library.spreads.sizing import cumulative_index, rolling_beta, size_pair


def _settings() -> Settings:
    return Settings(
        history_start="2020-01-01",
        history_end=None,
        on_server=True,
        cache_dir="cache",
        beta_window=5,
        vol_window=5,
        beta_lag=1,
        vol_lag=1,
        sparse_weekday_coverage=0.8,
        min_history_years=5,
        ffill_limit=5,
        tr_growth_gap=0.05,
        tr_field="TOT_RETURN_INDEX_GROSS_DVDS",
    )


def test_notional_is_long_minus_short() -> None:
    idx = pd.bdate_range("2020-01-01", periods=3)
    long = pd.Series([0.02, 0.00, -0.01], index=idx)
    short = pd.Series([0.01, 0.01, 0.01], index=idx)
    sized = size_pair(long, short, _settings(), "local")
    assert list(sized["ret_notional_local"].round(10)) == [0.01, -0.01, -0.02]


def test_beta_ignores_todays_return() -> None:
    idx = pd.bdate_range("2020-01-01", periods=8)
    # The short leg has to move. A constant short leg has no hedge ratio.
    short = pd.Series([0.01, -0.02, 0.015, -0.01, 0.02, 0.005, -0.03, 0.01], index=idx)
    long = 2.0 * short
    # Day index 5 is inside the window that will be used tomorrow, not today.
    long.iloc[5] = 1.0
    beta = rolling_beta(long, short, window=5, lag=1)
    assert pd.isna(beta.iloc[4])
    assert abs(beta.iloc[5] - 2.0) < 1e-9
    assert abs(beta.iloc[6] - 2.0) > 0.5


def test_equal_vols_match_notional_weights() -> None:
    idx = pd.bdate_range("2020-01-01", periods=12)
    long = pd.Series([0.01, -0.01] * 6, index=idx)
    short = pd.Series([-0.01, 0.01] * 6, index=idx)
    sized = size_pair(long, short, _settings(), "local")
    live = sized["w_long_vol_local"].dropna()
    assert abs(live.iloc[-1] - 1.0) < 1e-9
    assert abs(sized["w_short_vol_local"].dropna().iloc[-1] - 1.0) < 1e-9


def test_quieter_leg_gets_the_larger_weight() -> None:
    idx = pd.bdate_range("2020-01-01", periods=12)
    long = pd.Series([0.005, -0.005] * 6, index=idx)
    short = pd.Series([0.02, -0.02] * 6, index=idx)
    sized = size_pair(long, short, _settings(), "usd")
    assert sized["w_long_vol_usd"].dropna().iloc[-1] > sized["w_short_vol_usd"].dropna().iloc[-1]


def test_cumulative_index_compounds_and_skips_holes() -> None:
    idx = pd.bdate_range("2020-01-01", periods=3)
    returns = pd.Series([0.10, None, 0.10], index=idx)
    level = cumulative_index(returns)
    assert abs(level.iloc[0] - 110.0) < 1e-9
    assert pd.isna(level.iloc[1])
    assert abs(level.iloc[2] - 121.0) < 1e-9


def test_net_against_gross_is_named() -> None:
    assert net_vs_gross(["total_return_net", "total_return_gross"]) == "net_vs_gross"
    assert net_vs_gross(["total_return_net", "total_return"]) == "net_vs_gross"
    assert net_vs_gross(["price", "total_return_net"]) is None
    assert net_vs_gross(["total_return_gross", "total_return_gross"]) is None
