"""Thin wrap of desk_core.bloomberg.refdata.

desk_core is not modified. This module does not open its own blpapi session.

History requests are one ticker and one field at a time. desk_core.refdata.hist
loops internally, and a security error while reading fieldData aborts the whole
call, which would drop every later ticker in a batch. One security per call
keeps a bad symbol off the rest of the book. Reference-data snapshots do batch,
because that request returns an empty field set for an unknown security instead
of raising.
"""

from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Iterable, Sequence

import pandas as pd

logger = logging.getLogger(__name__)


def _as_date(value: date | datetime | str) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    if pd.isna(ts):
        raise ValueError(f"Could not parse date {value!r}")
    return ts.tz_localize(None) if ts.tzinfo else ts


class BloombergHistorySource:
    """BDH/BDP through desk_core, with a request counter for the log."""

    def __init__(self, *, on_server: bool = True) -> None:
        # Windows desk_core defaults to the desktop Terminal. This library is B-PIPE.
        self.on_server = on_server
        self.request_count = 0

    def hist(
        self,
        ticker: str,
        field: str,
        start: date | datetime | str,
        end: date | datetime | str,
    ) -> pd.DataFrame:
        """Return columns ``date`` and ``value``. Empty frame if Bloomberg has nothing."""
        from desk_core.bloomberg import refdata

        self.request_count += 1
        start_ts = _as_date(start)
        end_ts = _as_date(end)
        logger.info(
            "bbg hist #%s %s %s %s -> %s",
            self.request_count,
            ticker,
            field,
            start_ts.date(),
            end_ts.date(),
        )
        raw = refdata.hist(
            ticker,
            field,
            start_ts.to_pydatetime(),
            end_ts.to_pydatetime(),
            on_server=self.on_server,
        )
        return _normalize_hist(raw)

    def live(self, tickers: Sequence[str], fields: Sequence[str]) -> pd.DataFrame:
        """BDP snapshot. Not cached: names are stable, but the call is cheap and batched."""
        from desk_core.bloomberg import refdata

        self.request_count += 1
        logger.info("bbg live #%s n_tickers=%s fields=%s", self.request_count, len(tickers), list(fields))
        frame = refdata.live(list(tickers), list(fields), on_server=self.on_server)
        if frame is None or frame.empty:
            return pd.DataFrame(columns=list(fields))
        return frame


def _normalize_hist(raw: pd.DataFrame) -> pd.DataFrame:
    if raw is None or raw.empty:
        return pd.DataFrame(columns=["date", "value"])
    out = pd.DataFrame({"date": _naive_dates(raw["date"]), "value": pd.to_numeric(raw["value"], errors="coerce")})
    out = out.dropna(subset=["date"]).sort_values("date")
    # A ticker that only comes back as NaN is a failed pull, not a flat series.
    if out["value"].notna().sum() == 0:
        return pd.DataFrame(columns=["date", "value"])
    return out.drop_duplicates(subset=["date"], keep="last").reset_index(drop=True)


def _naive_dates(values: pd.Series) -> pd.Series:
    dates = pd.to_datetime(values)
    if getattr(dates.dt, "tz", None) is not None:
        dates = dates.dt.tz_convert(None)
    return dates.dt.normalize()


def chunked(items: Iterable[str], size: int) -> list[list[str]]:
    batch: list[str] = []
    groups: list[list[str]] = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            groups.append(batch)
            batch = []
    if batch:
        groups.append(batch)
    return groups
