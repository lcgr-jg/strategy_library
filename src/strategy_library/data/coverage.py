"""Sparse and short-history flags. A flagged series is kept and reported, not dropped."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class Coverage:
    n: int
    first: pd.Timestamp | None
    last: pd.Timestamp | None
    weekday_coverage: float | None
    years: float | None
    flags: tuple[str, ...]

    @property
    def status(self) -> str:
        if "empty" in self.flags:
            return "empty"
        if "short" in self.flags and "sparse" in self.flags:
            return "short_sparse"
        if "short" in self.flags:
            return "short"
        if "sparse" in self.flags:
            return "sparse"
        return "ok"


def cover(
    dates: pd.Series | pd.DatetimeIndex,
    *,
    min_years: float,
    min_coverage: float,
) -> Coverage:
    """Coverage against weekdays, not against an exchange calendar.

    A full equity series prints on about 96% of weekdays because of holidays.
    The 80% bar is there to catch holes, not Christmas.
    """
    index = pd.DatetimeIndex(pd.to_datetime(dates)).tz_localize(None).normalize()
    index = pd.DatetimeIndex(sorted(index.unique()))
    if len(index) == 0:
        return Coverage(0, None, None, None, None, ("empty",))
    first = index[0]
    last = index[-1]
    weekdays = pd.bdate_range(first, last)
    coverage = float(len(index) / len(weekdays)) if len(weekdays) else None
    years = float((last - first).days / 365.25)
    flags: list[str] = []
    if years < min_years:
        flags.append("short")
    if coverage is not None and coverage < min_coverage:
        flags.append("sparse")
    return Coverage(len(index), first, last, coverage, years, tuple(flags))
