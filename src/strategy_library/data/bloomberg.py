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
    """BDH/BDP through desk_core, with a request counter for the log.

    The default session is B-PIPE. A ticker is sent to the desktop Terminal only
    when B-PIPE answers NOT_ENTITLED. An unknown security stays on B-PIPE and
    comes back empty, so a bad ticker is not retried on the Terminal.
    """

    def __init__(self, *, on_server: bool = True) -> None:
        # Windows desk_core defaults to the desktop Terminal. This library is B-PIPE
        # except for the entitlement fallback below.
        self.on_server = on_server
        self.request_count = 0
        self.terminal_tickers: set[str] = set()
        self._prepared: set[str] = set()

    def prepare(self, tickers: Sequence[str]) -> None:
        """Learn which tickers B-PIPE will not entitle. One reference batch, no history."""
        unknown = [ticker for ticker in dict.fromkeys(tickers) if ticker not in self._prepared]
        for group in chunked(unknown, 25):
            # Entitlement is a property of the B-PIPE identity, so the check stays on B-PIPE
            # even when the later history pull for that name goes to the Terminal.
            statuses = self._reference_status(group, on_server=True)
            for ticker in group:
                self._prepared.add(ticker)
                if statuses.get(ticker) == "NOT_ENTITLED":
                    self.terminal_tickers.add(ticker)
        if self.terminal_tickers:
            logger.info("terminal fallback: %s", ", ".join(sorted(self.terminal_tickers)))

    def uses_terminal(self, ticker: str) -> bool:
        if ticker not in self._prepared:
            self.prepare([ticker])
        return ticker in self.terminal_tickers

    def hist(
        self,
        ticker: str,
        field: str,
        start: date | datetime | str,
        end: date | datetime | str,
    ) -> pd.DataFrame:
        """Return columns ``date`` and ``value``. Empty frame if Bloomberg has nothing."""
        from desk_core.bloomberg import refdata

        on_server = not self.uses_terminal(ticker)
        self.request_count += 1
        start_ts = _as_date(start)
        end_ts = _as_date(end)
        logger.info(
            "bbg hist #%s %s %s %s -> %s via %s",
            self.request_count,
            ticker,
            field,
            start_ts.date(),
            end_ts.date(),
            "B-PIPE" if on_server else "Terminal",
        )
        raw = refdata.hist(
            ticker,
            field,
            start_ts.to_pydatetime(),
            end_ts.to_pydatetime(),
            on_server=on_server,
        )
        return _normalize_hist(raw)

    def live(self, tickers: Sequence[str], fields: Sequence[str]) -> pd.DataFrame:
        """BDP snapshot. Not entitled names are snapshotted on the Terminal, not dropped."""
        from desk_core.bloomberg import refdata

        self.prepare(list(tickers))
        frames: list[pd.DataFrame] = []
        bpipe = [ticker for ticker in tickers if ticker not in self.terminal_tickers]
        terminal = [ticker for ticker in tickers if ticker in self.terminal_tickers]
        for group, on_server in ((bpipe, True), (terminal, False)):
            if not group:
                continue
            self.request_count += 1
            logger.info(
                "bbg live #%s n_tickers=%s fields=%s via %s",
                self.request_count,
                len(group),
                list(fields),
                "B-PIPE" if on_server else "Terminal",
            )
            frame = refdata.live(list(group), list(fields), on_server=on_server)
            if frame is not None and not frame.empty:
                frames.append(frame)
        if not frames:
            return pd.DataFrame(columns=list(fields))
        out = pd.concat(frames)
        return out[~out.index.duplicated(keep="first")]

    def _reference_status(self, tickers: Sequence[str], *, on_server: bool) -> dict[str, str]:
        """Read securityError, which refdata.live throws away.

        An empty NAME from refdata.live is how the first report called an entitled
        Terminal ticker a miss. The category on the existing desk_core session is
        the difference between NOT_ENTITLED and an invalid security.
        """
        from desk_core.bloomberg.session import get_session

        self.request_count += 1
        logger.info("bbg entitlement #%s n_tickers=%s", self.request_count, len(tickers))
        session = get_session(on_server=on_server)
        service = session._refdata_service()
        request = service.createRequest("ReferenceDataRequest")
        for ticker in tickers:
            request.getElement("securities").appendValue(ticker)
        request.getElement("fields").appendValue("NAME")
        session.session.sendRequest(request)
        import blpapi

        found: dict[str, str] = {}
        while True:
            event = session.session.nextEvent(500)
            for msg in event:
                if not msg.hasElement("securityData"):
                    continue
                for sec in msg.getElement("securityData").values():
                    ticker = sec.getElementAsString("security")
                    if sec.hasElement("securityError"):
                        err = sec.getElement("securityError")
                        found[ticker] = err.getElementAsString("category") if err.hasElement("category") else "ERROR"
                    else:
                        found[ticker] = "OK"
            if event.eventType() == blpapi.Event.RESPONSE:
                break
        return found


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
