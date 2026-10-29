"""Pull every configured series, cache it, and write the ticker report.

Failures stay in the report. A spread with a dead leg is not built and is not deleted
from the config. Probe tickers are snapshot-checked every run; history for a probe
is requested only when the snapshot returns a name.
"""

from __future__ import annotations

import logging
import sys
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from strategy_library.config import (  # noqa: E402
    PROJECT_ROOT,
    Factor,
    Spread,
    load_factors,
    load_fx,
    load_probe_tickers,
    load_settings,
    load_spreads,
    project_path,
)
from strategy_library.data.basis import growth_ratio
from strategy_library.data.bloomberg import BloombergHistorySource, chunked
from strategy_library.data.cache import ParquetCache
from strategy_library.data.coverage import cover
from strategy_library.data.panel import build_spread_frame
from strategy_library.data.store import CacheStore


def _jobs(spreads: tuple[Spread, ...], factors: tuple[Factor, ...], settings) -> list[tuple[str, str]]:
    found: set[tuple[str, str]] = set()

    def add(ticker: str | None, field: str) -> None:
        if ticker:
            found.add((ticker, field))

    for spread in spreads:
        for leg in spread.legs():
            add(leg.ticker, "PX_LAST")
            add(leg.tr_ticker, "PX_LAST")
            add(leg.tr_field and leg.ticker, leg.tr_field or "PX_LAST")
            add(leg.price_reference, "PX_LAST")
            # Performance indices (DAX, MDAX) are not stacked, but the field is still
            # measured so a double-counted dividend would show up in the report.
            if leg.basis in {"total_return", "total_return_gross", "total_return_net"}:
                add(leg.ticker, settings.tr_field)
        add(spread.vol_long, "PX_LAST")
        add(spread.vol_short, "PX_LAST")
    for factor in factors:
        add(factor.ticker, "PX_LAST")
    for quote in load_fx().values():
        add(quote.ticker, "PX_LAST")
    for ticker, field in (
        ("CPI CHNG Index", "PX_LAST"),
        ("CPI YOY Index", "PX_LAST"),
        ("NFP TCH Index", "PX_LAST"),
        ("CPI CHNG Index", "BN_SURVEY_MEDIAN"),
        ("CPI YOY Index", "BN_SURVEY_MEDIAN"),
        ("NFP TCH Index", "BN_SURVEY_MEDIAN"),
    ):
        add(ticker, field)
    return sorted(found)


def _snapshots(source: BloombergHistorySource, tickers: list[str]) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    fields = ["NAME", "CRNCY", "SECURITY_TYP", "PX_LAST"]
    for group in chunked(tickers, 25):
        try:
            frames.append(source.live(group, fields))
        except Exception:
            logging.exception("live batch failed; retrying one by one")
            for ticker in group:
                try:
                    frames.append(source.live([ticker], fields))
                except Exception as exc:
                    logging.error("live failed for %s: %s", ticker, exc)
    if not frames:
        return pd.DataFrame(columns=fields)
    out = pd.concat(frames)
    return out[~out.index.duplicated(keep="first")]


def _flags(status: str, raw: tuple[str, ...] | list[str]) -> str:
    flags = [flag for flag in raw if flag]
    if status == "monthly":
        return "monthly"
    if status == "stale" and "stale" not in flags:
        flags.append("stale")
    return ",".join(flags)


def _fmt_date(value: pd.Timestamp | None) -> str:
    if value is None or pd.isna(value):
        return ""
    return pd.Timestamp(value).strftime("%Y-%m-%d")


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_empty_"
    show = frame.fillna("")
    header = "| " + " | ".join(str(col) for col in show.columns) + " |"
    rule = "| " + " | ".join("---" for _ in show.columns) + " |"
    body = [
        "| " + " | ".join(str(value).replace("|", "/") for value in row) + " |"
        for row in show.itertuples(index=False, name=None)
    ]
    return "\n".join([header, rule, *body])


def _write_report(
    rows: pd.DataFrame,
    spread_rows: pd.DataFrame,
    probes: pd.DataFrame,
    request_count: int,
    path: Path,
) -> None:
    lines = [
        "# Ticker verification",
        "",
        f"Requests sent through desk_core: {request_count}.",
        "A series shorter than five years, or covering under 80% of weekdays between its first and last print, is flagged and kept.",
        "Weekdays are the denominator, so ordinary exchange holidays are not holes.",
        "",
        "## Series",
        "",
        _markdown_table(rows),
        "",
        "## Spreads",
        "",
        _markdown_table(spread_rows),
        "",
        "## Probes that did not resolve",
        "",
    ]
    name_col = "NAME" if "NAME" in probes.columns else None
    dead = probes[probes[name_col].isna()] if name_col and not probes.empty else probes.iloc[0:0]
    if dead.empty:
        lines.append("None.")
    else:
        lines.append(", ".join(dead.index.astype(str)))
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    settings = load_settings()
    spreads = load_spreads()
    factors = load_factors()
    fx = load_fx()
    end = settings.history_end or date.today().isoformat()
    start = settings.history_start
    source = BloombergHistorySource(on_server=settings.on_server)
    cache = ParquetCache(project_path(settings.cache_dir), source)

    probe_tickers = list(load_probe_tickers())
    configured = sorted({ticker for ticker, _ in _jobs(spreads, factors, settings)})
    logging.info("snapshot %s tickers", len(set(configured) | set(probe_tickers)))
    snaps = _snapshots(source, sorted(set(configured) | set(probe_tickers)))
    named = set()
    if not snaps.empty and "NAME" in snaps.columns:
        named = set(snaps.index[snaps["NAME"].notna()].astype(str))

    rows: list[dict] = []
    for ticker, field in _jobs(spreads, factors, settings):
        # Configured series are always requested. A blank snapshot must not hide a history entitlement.
        try:
            frame = cache.get(ticker, field, start, end)
        except Exception as exc:
            rows.append({"ticker": ticker, "field": field, "status": "error", "detail": str(exc)[:200]})
            continue
        stats = cover(
            frame["date"] if not frame.empty else [],
            min_years=settings.min_history_years,
            min_coverage=settings.sparse_weekday_coverage,
        )
        # An exception inside the cache is recorded as a note and comes back empty.
        # Surface it. An empty parquet is not written, so this is not a cached failure.
        failure = next(
            (note.detail for note in reversed(cache.notes) if note.ticker == ticker and note.field == field and note.status == "error"),
            "",
        )
        if failure and stats.status == "empty":
            status = "error"
        elif (
            stats.status == "sparse"
            and stats.years
            and stats.n
            and 8 <= stats.n / stats.years <= 16
        ):
            # CPI and NFP print once a month. The weekday rule is for daily equity series.
            status = "monthly"
        else:
            status = stats.status
        # Coverage is measured inside the printed span, so a series that died in 2023
        # still looks complete. Flag that separately. 45 days keeps a monthly release
        # that printed last month from being called dead.
        if stats.last is not None and (pd.Timestamp(end) - stats.last).days > 45 and status == "ok":
            status = "stale"
        name = ""
        currency = ""
        if not snaps.empty and ticker in snaps.index:
            name = snaps.at[ticker, "NAME"] if "NAME" in snaps.columns else ""
            currency = snaps.at[ticker, "CRNCY"] if "CRNCY" in snaps.columns else ""
        rows.append(
            {
                "ticker": ticker,
                "field": field,
                "name": "" if pd.isna(name) else name,
                "currency": "" if pd.isna(currency) else currency,
                "status": status,
                "detail": failure,
                "n": stats.n,
                "first": _fmt_date(stats.first),
                "last": _fmt_date(stats.last),
                "years": None if stats.years is None else round(stats.years, 2),
                "weekday_coverage": None if stats.weekday_coverage is None else round(stats.weekday_coverage, 3),
                "flags": _flags(status, stats.flags),
            }
        )

    for ticker in probe_tickers:
        if ticker in named and (ticker, "PX_LAST") not in {(row["ticker"], row["field"]) for row in rows}:
            frame = cache.get(ticker, "PX_LAST", start, end)
            stats = cover(frame["date"] if not frame.empty else [], min_years=settings.min_history_years, min_coverage=settings.sparse_weekday_coverage)
            probe_status = stats.status
            if stats.last is not None and (pd.Timestamp(end) - stats.last).days > 45 and probe_status == "ok":
                probe_status = "stale"
            rows.append(
                {
                    "ticker": ticker,
                    "field": "PX_LAST",
                    "name": snaps.at[ticker, "NAME"],
                    "currency": snaps.at[ticker, "CRNCY"] if "CRNCY" in snaps.columns else "",
                    "status": probe_status,
                    "detail": "",
                    "n": stats.n,
                    "first": _fmt_date(stats.first),
                    "last": _fmt_date(stats.last),
                    "years": None if stats.years is None else round(stats.years, 2),
                    "weekday_coverage": None if stats.weekday_coverage is None else round(stats.weekday_coverage, 3),
                    "flags": _flags(probe_status, ("probe", *stats.flags)),
                }
            )

    store = CacheStore(cache)
    fx_levels = {quote.ticker: store.levels(quote.ticker, "PX_LAST", start, end) for quote in fx.values()}
    spread_rows: list[dict] = []
    panel_dir = project_path(settings.cache_dir) / "panels"
    panel_dir.mkdir(parents=True, exist_ok=True)
    for spread in spreads:
        try:
            frame, builds, warning = build_spread_frame(
                spread, store, settings, fx, fx_levels, start=start, end=end
            )
        except Exception as exc:
            logging.exception("panel failed for %s", spread.id)
            spread_rows.append({"id": spread.id, "rows": 0, "warning": f"error: {exc}"[:300], "built": False})
            continue
        empty_legs = [build.leg.ticker for build in builds if build.choice.levels.dropna().empty]
        bases = ", ".join(f"{build.leg.ticker}={build.choice.basis}/{build.choice.source}" for build in builds)
        growths = []
        for build in builds:
            price = store.levels(build.leg.ticker, "PX_LAST", start, end)
            used = build.choice.levels
            price_g = growth_ratio(price)
            used_g = growth_ratio(used)
            if price_g and used_g:
                growths.append(f"{build.leg.ticker}:{used_g / price_g - 1:.1%}")
        built = not empty_legs and not frame.dropna(how="all").empty
        if built:
            frame.to_parquet(panel_dir / f"{spread.id}.parquet")
        spread_rows.append(
            {
                "id": spread.id,
                "alignment": spread.alignment,
                "rows": int(frame.dropna(how="all").shape[0]),
                "built": built,
                "empty_legs": ",".join(empty_legs),
                "bases": bases,
                "tr_vs_price": ", ".join(growths),
                "warning": warning or "",
            }
        )

    report = pd.DataFrame(rows).sort_values(["status", "ticker", "field"])
    spread_report = pd.DataFrame(spread_rows)
    reports = project_path("reports")
    reports.mkdir(parents=True, exist_ok=True)
    report.to_csv(reports / "ticker_verification.csv", index=False)
    spread_report.to_csv(reports / "spread_verification.csv", index=False)
    _write_report(report, spread_report, snaps, source.request_count, reports / "ticker_verification.md")
    logging.info(
        "done requests=%s series=%s spreads_built=%s",
        source.request_count,
        len(report),
        int(spread_report["built"].sum()) if not spread_report.empty else 0,
    )
    print(report.to_string(index=False))
    print(spread_report.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
