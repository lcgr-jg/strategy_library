"""Asia is aligned onto the previous US session. Holidays inside the limit are zeros."""

from __future__ import annotations

import pandas as pd

from strategy_library.data.calendar import (
    native_returns,
    place_returns,
    shift_asian_returns_to_prior_anchor,
)


def test_asian_return_lands_on_the_previous_us_session() -> None:
    # Wednesday US CPI is answered by Thursday's Tokyo session.
    us = pd.to_datetime(["2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12"])
    japan = pd.Series(
        [0.01, 0.02],
        index=pd.to_datetime(["2024-01-09", "2024-01-10"]),
    )
    shifted = shift_asian_returns_to_prior_anchor(japan, pd.DatetimeIndex(us))
    assert abs(shifted.loc[pd.Timestamp("2024-01-08")] - 0.01) < 1e-12
    assert abs(shifted.loc[pd.Timestamp("2024-01-09")] - 0.02) < 1e-12


def test_us_holiday_compounds_two_asian_sessions() -> None:
    # US shut on Wednesday. Tuesday receives both Wednesday and Thursday Tokyo.
    us = pd.to_datetime(["2024-01-09", "2024-01-11"])
    japan = pd.Series([0.10, 0.10], index=pd.to_datetime(["2024-01-10", "2024-01-11"]))
    shifted = shift_asian_returns_to_prior_anchor(japan, pd.DatetimeIndex(us))
    assert len(shifted) == 1
    assert abs(shifted.loc[pd.Timestamp("2024-01-09")] - ((1.1 * 1.1) - 1)) < 1e-12


def test_closed_session_inside_limit_is_zero() -> None:
    levels = pd.Series([100.0, 110.0], index=pd.to_datetime(["2024-01-04", "2024-01-08"]))
    native = native_returns(levels)
    calendar = pd.to_datetime(["2024-01-04", "2024-01-05", "2024-01-08"])
    # The Jan 4 print has no return of its own. It still has to anchor Friday's zero.
    placed = place_returns(
        native,
        pd.DatetimeIndex(calendar),
        ffill_limit=5,
        sessions=pd.DatetimeIndex(levels.index),
    )
    assert placed.loc[pd.Timestamp("2024-01-05")] == 0.0
    assert abs(placed.loc[pd.Timestamp("2024-01-08")] - 0.10) < 1e-12


def test_long_hole_is_not_filled_with_zeros() -> None:
    native = pd.Series([0.01], index=pd.to_datetime(["2024-01-02"]))
    calendar = pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08", "2024-01-09"])
    placed = place_returns(native, pd.DatetimeIndex(calendar), ffill_limit=2)
    assert placed.loc[pd.Timestamp("2024-01-03")] == 0.0
    assert placed.loc[pd.Timestamp("2024-01-04")] == 0.0
    assert pd.isna(placed.loc[pd.Timestamp("2024-01-08")])
