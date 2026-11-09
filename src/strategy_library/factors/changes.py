"""Turn cached factor levels into the changes the regressions use.

The transform is the one written on the factor. Yields stay in percentage
points. A beta on a yield is spread return per 1 point, not per basis point.
This module does not rescale them.
"""

from __future__ import annotations

import pandas as pd

from strategy_library.config import Factor


def transform_level(levels: pd.Series, transform: str) -> pd.Series:
    """Daily change on the factor's own sessions. A missing print is not filled."""
    clean = levels.dropna().sort_index()
    clean = clean[~clean.index.duplicated(keep="last")]
    if transform == "diff":
        return clean.diff()
    if transform == "pct":
        return clean.pct_change()
    raise ValueError(f"transform must be diff or pct, got {transform!r}")


def _slope(left: pd.Series, right: pd.Series) -> pd.Series:
    """First series minus second, on days both printed.

    For 2s10s the config lists the 10y first and the 2y second, so the level
    is the 10y yield minus the 2y yield. Differencing that level is the change
    the regression sees.
    """
    both = pd.concat({"left": left, "right": right}, axis=1).dropna()
    return both["left"] - both["right"]


def build_factor_changes(
    levels: dict[str, pd.Series],
    factors: tuple[Factor, ...],
) -> pd.DataFrame:
    """One column per factor id. The index is the union of the factor calendars.

    ``levels`` is keyed by ticker. A derived factor reads earlier factor levels
    by id, so the 10y and the 2y have to appear before the slope.
    """
    levels_by_id: dict[str, pd.Series] = {}
    changes: dict[str, pd.Series] = {}
    for factor in factors:
        if factor.derived:
            left_id, right_id = factor.derived
            if left_id not in levels_by_id or right_id not in levels_by_id:
                raise KeyError(f"{factor.id} needs {left_id} and {right_id} earlier in the factor list")
            level = _slope(levels_by_id[left_id], levels_by_id[right_id])
        else:
            if factor.ticker not in levels:
                raise KeyError(f"{factor.id} has no level series for {factor.ticker}")
            level = levels[factor.ticker]
        levels_by_id[factor.id] = level
        changes[factor.id] = transform_level(level, factor.transform).rename(factor.id)
    if not changes:
        return pd.DataFrame()
    return pd.concat(changes.values(), axis=1).sort_index()
