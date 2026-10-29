"""Session alignment.

Each leg's return is computed on the days that leg actually traded. Those
returns are then placed on the spread calendar. A day the leg was shut is a
zero return, and only for a few sessions. A longer hole stays missing so a
dead feed is not turned into a flat market.

Asia versus the US
------------------
Tokyo, Hong Kong and Sydney are already closed before the US cash open, and
long before a US data release. The Asian session that can react to Wednesday's
US news is Thursday's Asian session.

``asia_to_us`` stamps that Thursday Asian return onto Wednesday's US date.
The Asian return dated D is placed on the last US session strictly before D.
If a US holiday swallows two Asian sessions, those simple returns are
compounded onto the single prior US date rather than dropped.

Same-region spreads, including Japan versus Japan, stay on ``native`` alignment.
US event studies can still call :func:`shift_asian_returns_to_prior_anchor`
later even when the spread's own default is native. MSCI EM is left on native
alignment: the index is struck around the US close and already contains that
day's Asian closes, so a second shift would move Asia twice.
"""

from __future__ import annotations

import pandas as pd

ASIA_REGIONS = frozenset({"JP", "HK", "AU"})


def native_returns(levels: pd.Series) -> pd.Series:
    """Simple close-to-close return on the dates present in ``levels``."""
    clean = levels.dropna().sort_index()
    clean.index = pd.to_datetime(clean.index).tz_localize(None).normalize()
    rets = clean.pct_change()
    return rets.dropna()


def shift_asian_returns_to_prior_anchor(
    asian_returns: pd.Series,
    anchor_sessions: pd.DatetimeIndex,
) -> pd.Series:
    """Move each Asian return onto the previous anchor session.

    See the module note for why the shift is backward by one anchor session
    and not forward by one calendar day.
    """
    asian = asian_returns.dropna().sort_index()
    if asian.empty:
        return asian
    anchor = pd.DatetimeIndex(pd.to_datetime(anchor_sessions)).tz_localize(None).normalize()
    anchor = pd.DatetimeIndex(sorted(anchor.unique()))
    # searchsorted(..., side="left") - 1 is the last anchor date strictly before the Asian print.
    positions = anchor.searchsorted(asian.index, side="left") - 1
    keep = positions >= 0
    if not keep.any():
        return pd.Series(dtype=float)
    targets = anchor[positions[keep]]
    moved = pd.Series(asian.to_numpy()[keep], index=pd.DatetimeIndex(targets))
    # Two Asian sessions can land on one anchor date across a US holiday.
    # Compound them so Thursday's move is not thrown away when Wednesday was shut.
    return moved.groupby(level=0).apply(lambda chunk: float((1.0 + chunk).prod() - 1.0)).sort_index()


def place_returns(
    native: pd.Series,
    calendar: pd.DatetimeIndex,
    *,
    ffill_limit: int,
    sessions: pd.DatetimeIndex | None = None,
) -> pd.Series:
    """Put native returns on ``calendar``. Closed sessions inside the limit are 0.

    ``sessions`` are the dates the leg actually printed a level. The first print
    has no return, but it is still the anchor for the holiday that follows it.
    Without that anchor, the gap between the first two observations stays missing
    and a one-day holiday looks like a hole in the basket.

    The limit is counted in spread sessions, not raw calendar days, because a
    weekend is already absent from the spread calendar and should not use up
    the holiday bridge.
    """
    points = native.dropna().sort_index()
    calendar = pd.DatetimeIndex(pd.to_datetime(calendar)).tz_localize(None).normalize()
    calendar = pd.DatetimeIndex(sorted(calendar.unique()))
    out = points.reindex(calendar)
    session_index = points.index if sessions is None else pd.DatetimeIndex(pd.to_datetime(sessions)).tz_localize(None).normalize()
    session_index = pd.DatetimeIndex(sorted(session_index.unique()))
    if session_index.empty or ffill_limit <= 0:
        return out
    cal_pos = {day: i for i, day in enumerate(calendar)}
    for day in calendar:
        if pd.notna(out.loc[day]):
            continue
        pos = int(session_index.searchsorted(pd.Timestamp(day), side="left")) - 1
        if pos < 0:
            continue
        prev = pd.Timestamp(session_index[pos])
        if prev not in cal_pos or day not in cal_pos:
            continue
        gap = cal_pos[day] - cal_pos[prev]
        if 0 < gap <= ffill_limit:
            out.loc[day] = 0.0
    return out


def union_calendar(series: list[pd.Series]) -> pd.DatetimeIndex:
    dates: list[pd.Timestamp] = []
    for item in series:
        if item is None or item.empty:
            continue
        dates.extend(pd.to_datetime(item.index).tz_localize(None).normalize().tolist())
    if not dates:
        return pd.DatetimeIndex([])
    return pd.DatetimeIndex(sorted(set(dates)))
