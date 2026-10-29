"""Parquet cache keyed by ticker and field, not by the requested window.

One file holds the whole series. A later run fetches only the dates outside
the stored range. An empty tail (a holiday, or today before the print) is
remembered via checked_through so the same gap is not requested again.

A ticker that has never returned a row is not written. The next run retries it.
Freezing a permission failure as an empty parquet would hide a later entitlement.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Protocol

import pandas as pd

logger = logging.getLogger(__name__)


class HistorySource(Protocol):
    request_count: int

    def hist(
        self,
        ticker: str,
        field: str,
        start: date | datetime | str,
        end: date | datetime | str,
    ) -> pd.DataFrame:
        """Long frame with columns date, value."""


def _stamp(value: date | datetime | str) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    if pd.isna(ts):
        raise ValueError(f"Could not parse date {value!r}")
    if ts.tzinfo is not None:
        ts = ts.tz_localize(None)
    return ts.normalize()


def _safe(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())[:80]


@dataclass
class FetchNote:
    ticker: str
    field: str
    status: str
    detail: str = ""


class ParquetCache:
    def __init__(self, root: Path, source: HistorySource) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.source = source
        self.manifest_path = self.root / "manifest.json"
        self._manifest = self._read_manifest()
        self.notes: list[FetchNote] = []
        # A ticker with no rows is not written to disk, so the next process retries it.
        # Within this process, remember the miss. Otherwise one spread build asks again
        # for every leg that shares the dead symbol.
        self._session_miss: set[tuple[str, str]] = set()

    def path_for(self, ticker: str, field: str) -> Path:
        return self.root / f"{_safe(ticker)}__{_safe(field)}.parquet"

    def get(
        self,
        ticker: str,
        field: str,
        start: date | datetime | str,
        end: date | datetime | str,
        *,
        force: bool = False,
    ) -> pd.DataFrame:
        """Return the cached series sliced to ``[start, end]``, filling only missing edges."""
        start_ts = _stamp(start)
        end_ts = _stamp(end)
        if end_ts < start_ts:
            raise ValueError(f"{ticker} {field}: end {end_ts.date()} is before start {start_ts.date()}")
        key = self._key(ticker, field)
        if force:
            self._drop(ticker, field)
            self._session_miss.discard((ticker, field))
        elif (ticker, field) in self._session_miss:
            return pd.DataFrame(columns=["date", "value"])

        cached = self._read(ticker, field)
        meta = self._manifest.get(key, {})
        ranges = self._missing_ranges(cached, meta, start_ts, end_ts)
        for gap_start, gap_end in ranges:
            try:
                fetched = self.source.hist(ticker, field, gap_start, gap_end)
            except Exception as exc:  # one security must not kill the book
                logger.exception("bbg hist failed for %s %s", ticker, field)
                self.notes.append(
                    FetchNote(ticker, field, "error", str(exc).splitlines()[0][:300])
                )
                continue
            fetched = self._clean(fetched)
            if not fetched.empty:
                cached = self._merge(cached, fetched)
            # Remember the window we asked for even when the tail is a holiday,
            # but only once the series itself exists. A never-seen ticker stays
            # uncached so the next run retries a bad symbol.
            if not cached.empty:
                self._mark_checked(key, gap_start, gap_end)
                self._write(ticker, field, cached)
                self.notes.append(
                    FetchNote(ticker, field, "fetched", f"{gap_start.date()} {gap_end.date()} rows={len(fetched)}")
                )
            else:
                self.notes.append(FetchNote(ticker, field, "empty", f"{gap_start.date()} {gap_end.date()}"))

        if cached.empty:
            self._session_miss.add((ticker, field))
            return cached
        mask = (cached["date"] >= start_ts) & (cached["date"] <= end_ts)
        return cached.loc[mask].reset_index(drop=True)

    def _missing_ranges(
        self,
        cached: pd.DataFrame,
        meta: dict,
        start: pd.Timestamp,
        end: pd.Timestamp,
    ) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
        if cached.empty:
            return [(start, end)]
        first = cached["date"].min()
        last = cached["date"].max()
        checked_from = _stamp(meta["checked_from"]) if meta.get("checked_from") else first
        checked_through = _stamp(meta["checked_through"]) if meta.get("checked_through") else last
        gaps: list[tuple[pd.Timestamp, pd.Timestamp]] = []
        # Head: Bloomberg omits the years before a series was listed. checked_from
        # is the earliest date we already asked for, which may be before the first print.
        if start < checked_from:
            gaps.append((start, min(end, checked_from - pd.Timedelta(days=1))))
        if end > checked_through:
            gap_start = max(start, last + pd.Timedelta(days=1))
            if gap_start <= end:
                gaps.append((gap_start, end))
        return [(a, b) for a, b in gaps if a <= b]

    def _mark_checked(self, key: str, start: pd.Timestamp, end: pd.Timestamp) -> None:
        meta = dict(self._manifest.get(key, {}))
        prev_from = _stamp(meta["checked_from"]) if meta.get("checked_from") else start
        prev_through = _stamp(meta["checked_through"]) if meta.get("checked_through") else end
        meta["checked_from"] = min(prev_from, start).strftime("%Y-%m-%d")
        meta["checked_through"] = max(prev_through, end).strftime("%Y-%m-%d")
        self._manifest[key] = meta
        self._write_manifest()

    @staticmethod
    def _key(ticker: str, field: str) -> str:
        return f"{ticker}|{field}"

    def _drop(self, ticker: str, field: str) -> None:
        path = self.path_for(ticker, field)
        if path.exists():
            path.unlink()
        self._manifest.pop(self._key(ticker, field), None)
        self._write_manifest()

    def _read(self, ticker: str, field: str) -> pd.DataFrame:
        path = self.path_for(ticker, field)
        if not path.exists():
            return pd.DataFrame(columns=["date", "value"])
        frame = pd.read_parquet(path)
        return self._clean(frame)

    def _write(self, ticker: str, field: str, frame: pd.DataFrame) -> None:
        clean = self._clean(frame)
        clean.to_parquet(self.path_for(ticker, field), index=False)

    @staticmethod
    def _clean(frame: pd.DataFrame) -> pd.DataFrame:
        if frame is None or frame.empty:
            return pd.DataFrame(columns=["date", "value"])
        dates = pd.to_datetime(frame["date"])
        if getattr(dates.dt, "tz", None) is not None:
            dates = dates.dt.tz_convert(None)
        out = pd.DataFrame(
            {
                "date": dates.dt.normalize(),
                "value": pd.to_numeric(frame["value"], errors="coerce"),
            }
        )
        out = out.dropna(subset=["value"]).drop_duplicates(subset=["date"], keep="last")
        return out.sort_values("date").reset_index(drop=True)

    @staticmethod
    def _merge(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
        if left.empty:
            return right
        if right.empty:
            return left
        return (
            pd.concat([left, right], ignore_index=True)
            .drop_duplicates(subset=["date"], keep="last")
            .sort_values("date")
            .reset_index(drop=True)
        )

    def _read_manifest(self) -> dict:
        if not self.manifest_path.exists():
            return {}
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def _write_manifest(self) -> None:
        self.manifest_path.write_text(json.dumps(self._manifest, indent=2, sort_keys=True), encoding="utf-8")
