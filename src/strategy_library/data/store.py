"""Cache-backed level store. Panels ask for series; they do not talk to Bloomberg."""

from __future__ import annotations

import pandas as pd

from strategy_library.data.cache import ParquetCache
from strategy_library.data.panel import LevelStore


class CacheStore(LevelStore):
    def __init__(self, cache: ParquetCache) -> None:
        self.cache = cache

    def levels(self, ticker: str, field: str, start: str, end: str) -> pd.Series:
        frame = self.cache.get(ticker, field, start, end)
        if frame.empty:
            return pd.Series(dtype=float, name=ticker)
        series = pd.Series(frame["value"].to_numpy(), index=pd.to_datetime(frame["date"]), name=ticker)
        series.index = series.index.tz_localize(None).normalize()
        return series.sort_index()
