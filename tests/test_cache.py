"""Cache behaviour with an in-memory source. No Bloomberg."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from strategy_library.data.cache import ParquetCache


class FakeSource:
    def __init__(self, frames: dict[tuple[str, str], pd.DataFrame]) -> None:
        self.frames = frames
        self.calls: list[tuple[str, str, str, str]] = []
        self.request_count = 0

    def hist(self, ticker: str, field: str, start, end) -> pd.DataFrame:
        self.request_count += 1
        self.calls.append((ticker, field, str(pd.Timestamp(start).date()), str(pd.Timestamp(end).date())))
        frame = self.frames.get((ticker, field), pd.DataFrame(columns=["date", "value"]))
        if frame.empty:
            return frame
        start_ts = pd.Timestamp(start).normalize()
        end_ts = pd.Timestamp(end).normalize()
        mask = (frame["date"] >= start_ts) & (frame["date"] <= end_ts)
        return frame.loc[mask].reset_index(drop=True)


def _frame(days: list[str], values: list[float]) -> pd.DataFrame:
    return pd.DataFrame({"date": pd.to_datetime(days), "value": values})


def test_second_call_does_not_refetch(tmp_path: Path) -> None:
    source = FakeSource({("SPX Index", "PX_LAST"): _frame(["2020-01-02", "2020-01-03"], [1.0, 2.0])})
    cache = ParquetCache(tmp_path, source)
    first = cache.get("SPX Index", "PX_LAST", "2020-01-02", "2020-01-03")
    second = cache.get("SPX Index", "PX_LAST", "2020-01-02", "2020-01-03")
    assert len(source.calls) == 1
    assert list(first["value"]) == [1.0, 2.0]
    assert list(second["value"]) == [1.0, 2.0]


def test_wider_end_fetches_only_the_tail(tmp_path: Path) -> None:
    source = FakeSource({("SPX Index", "PX_LAST"): _frame(["2020-01-02", "2020-01-03", "2020-01-06"], [1.0, 2.0, 3.0])})
    cache = ParquetCache(tmp_path, source)
    cache.get("SPX Index", "PX_LAST", "2020-01-02", "2020-01-03")
    cache.get("SPX Index", "PX_LAST", "2020-01-02", "2020-01-06")
    assert source.calls[1][2] == "2020-01-04"
    assert source.calls[1][3] == "2020-01-06"


def test_empty_head_is_not_requested_again(tmp_path: Path) -> None:
    # Series starts in 2010. The 2005 request is remembered so the next run does not walk the empty years.
    source = FakeSource({("NKY Index", "PX_LAST"): _frame(["2010-01-04", "2010-01-05"], [10.0, 11.0])})
    cache = ParquetCache(tmp_path, source)
    cache.get("NKY Index", "PX_LAST", "2005-01-01", "2010-01-05")
    cache.get("NKY Index", "PX_LAST", "2005-01-01", "2010-01-05")
    assert len(source.calls) == 1


def test_empty_ticker_is_not_frozen_but_not_repeated_in_one_run(tmp_path: Path) -> None:
    source = FakeSource({})
    cache = ParquetCache(tmp_path, source)
    empty = cache.get("IBOV Index", "PX_LAST", "2020-01-01", "2020-01-10")
    assert empty.empty
    assert not cache.path_for("IBOV Index", "PX_LAST").exists()
    # Same process: do not ask Bloomberg again for a symbol that just came back empty.
    cache.get("IBOV Index", "PX_LAST", "2020-01-01", "2020-01-10")
    assert len(source.calls) == 1
    # Next process: retry, because an empty miss is not written to disk.
    ParquetCache(tmp_path, source).get("IBOV Index", "PX_LAST", "2020-01-01", "2020-01-10")
    assert len(source.calls) == 2


def test_holiday_tail_is_not_refetched(tmp_path: Path) -> None:
    source = FakeSource({("SPX Index", "PX_LAST"): _frame(["2020-01-02", "2020-01-03"], [1.0, 2.0])})
    cache = ParquetCache(tmp_path, source)
    cache.get("SPX Index", "PX_LAST", "2020-01-02", "2020-01-08")
    cache.get("SPX Index", "PX_LAST", "2020-01-02", "2020-01-08")
    assert len(source.calls) == 1


def test_failed_request_does_not_wipe_cache(tmp_path: Path) -> None:
    source = FakeSource({("SPX Index", "PX_LAST"): _frame(["2020-01-02"], [1.0])})
    cache = ParquetCache(tmp_path, source)
    cache.get("SPX Index", "PX_LAST", "2020-01-02", "2020-01-02")

    class Boom(FakeSource):
        def hist(self, ticker, field, start, end):
            self.request_count += 1
            raise RuntimeError("b-pipe down")

    broken = Boom({})
    again = ParquetCache(tmp_path, broken)
    out = again.get("SPX Index", "PX_LAST", "2020-01-02", "2020-01-06")
    assert list(out["value"]) == [1.0]
    assert again.notes[0].status == "error"
