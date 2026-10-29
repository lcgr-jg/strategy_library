"""Build aligned leg returns for one spread. Sizing weights are Phase 2.

The basket inside a side is an equal weight of simple returns, and a day is
kept only when every sleeve printed (or was bridged). Skipping a missing
sleeve would silently double the others.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from strategy_library.config import FxQuote, Leg, Settings, Spread
from strategy_library.data.basis import SeriesChoice, choose_levels, mixed_basis
from strategy_library.data.calendar import (
    ASIA_REGIONS,
    native_returns,
    place_returns,
    shift_asian_returns_to_prior_anchor,
    union_calendar,
)
from strategy_library.data.fx import levels_to_usd


@dataclass(frozen=True)
class LegBuild:
    leg: Leg
    choice: SeriesChoice
    ret_local: pd.Series
    ret_usd: pd.Series


class LevelStore:
    """Anything that can hand back a date-indexed level series."""

    def levels(self, ticker: str, field: str, start: str, end: str) -> pd.Series:
        raise NotImplementedError


def _fx_on_dates(levels: pd.Series, fx: pd.Series, *, ffill_limit: int) -> pd.Series:
    """Carry the last FX print across a short holiday so a shut FX market does not drop the equity day."""
    if fx is None or fx.dropna().empty:
        return pd.Series(dtype=float)
    aligned = fx.sort_index().reindex(fx.index.union(levels.index)).sort_index()
    aligned = aligned.ffill(limit=ffill_limit)
    return aligned.reindex(levels.index)


def build_leg(
    leg: Leg,
    store: LevelStore,
    settings: Settings,
    fx_quotes: dict[str, FxQuote],
    fx_levels: dict[str, pd.Series],
    *,
    start: str,
    end: str,
) -> LegBuild:
    price = store.levels(leg.ticker, "PX_LAST", start, end)
    total_return: pd.Series | None = None
    source_label = "price"
    if leg.tr_ticker:
        total_return = store.levels(leg.tr_ticker, "PX_LAST", start, end)
        source_label = leg.tr_ticker
    elif leg.tr_field and leg.basis not in {"total_return", "total_return_gross", "total_return_net"}:
        total_return = store.levels(leg.ticker, leg.tr_field, start, end)
        source_label = leg.tr_field
    # basis on a leg that also names tr_ticker describes that total-return index.
    # basis without a total-return ticker or field means the price ticker is already
    # a performance index (DAX). Those are different facts and must not share a branch.
    price_is_already = (
        not leg.tr_ticker
        and not leg.tr_field
        and leg.basis in {"total_return", "total_return_gross", "total_return_net"}
    )
    choice = choose_levels(
        price=price,
        total_return=total_return,
        configured_basis=leg.basis,
        gap=settings.tr_growth_gap,
        source_label=source_label,
        dedicated=bool(leg.tr_ticker),
        price_is_already_total_return=price_is_already,
    )
    if leg.instrument == "etf" and choice.basis == "price":
        # ETF PX_LAST drops distributed dividends. Say so; do not pretend it is a total-return index.
        choice = SeriesChoice(choice.levels, "etf_price", choice.source, choice.note + "; ETF price is not dividend-reinvested")
    local = native_returns(choice.levels)
    usd_levels = _usd_levels(choice.levels, leg, fx_quotes, fx_levels, settings.ffill_limit)
    usd = native_returns(usd_levels) if leg.currency and leg.currency != "USD" else local.copy()
    return LegBuild(leg=leg, choice=choice, ret_local=local, ret_usd=usd)


def _usd_levels(
    levels: pd.Series,
    leg: Leg,
    fx_quotes: dict[str, FxQuote],
    fx_levels: dict[str, pd.Series],
    ffill_limit: int,
) -> pd.Series:
    if not leg.currency or leg.currency == "USD":
        return levels
    quote = fx_quotes[leg.currency]
    fx = _fx_on_dates(levels, fx_levels.get(quote.ticker, pd.Series(dtype=float)), ffill_limit=ffill_limit)
    return levels_to_usd(levels, fx, quote)


def _equal_weight(parts: list[pd.Series]) -> pd.Series:
    if not parts:
        return pd.Series(dtype=float)
    frame = pd.concat(parts, axis=1)
    # min_count keeps a one-sleeve holiday from rescaling the basket.
    return frame.mean(axis=1, skipna=True).where(frame.notna().sum(axis=1) >= len(parts))


def _prepare_side(
    builds: list[LegBuild],
    *,
    which: str,
    alignment: str,
    anchor: pd.DatetimeIndex,
    ffill_limit: int,
    calendar: pd.DatetimeIndex,
) -> tuple[pd.Series, pd.Series, list[str]]:
    local_parts: list[pd.Series] = []
    usd_parts: list[pd.Series] = []
    bases: list[str] = []
    for build in builds:
        local = build.ret_local
        usd = build.ret_usd
        region = build.leg.region or ""
        shifted = alignment == "asia_to_us" and region in ASIA_REGIONS and len(anchor)
        if shifted:
            local = shift_asian_returns_to_prior_anchor(local, anchor)
            usd = shift_asian_returns_to_prior_anchor(usd, anchor)
        # After the shift, the sessions that matter are the anchor dates we just wrote.
        # Before the shift, the level dates include the first print, which has no return
        # but still anchors the following holiday.
        local_sessions = local.dropna().index if shifted else build.choice.levels.dropna().index
        usd_sessions = usd.dropna().index if shifted else local_sessions
        local_parts.append(place_returns(local, calendar, ffill_limit=ffill_limit, sessions=local_sessions).rename(which))
        usd_parts.append(place_returns(usd, calendar, ffill_limit=ffill_limit, sessions=usd_sessions).rename(which))
        bases.append(build.choice.basis)
    return _equal_weight(local_parts), _equal_weight(usd_parts), bases


def build_spread_frame(
    spread: Spread,
    store: LevelStore,
    settings: Settings,
    fx_quotes: dict[str, FxQuote],
    fx_levels: dict[str, pd.Series],
    *,
    start: str,
    end: str,
) -> tuple[pd.DataFrame, list[LegBuild], str | None]:
    """Return the aligned return frame, the per-leg builds, and a basis warning."""
    builds = [
        build_leg(leg, store, settings, fx_quotes, fx_levels, start=start, end=end)
        for leg in spread.legs()
    ]
    long_builds = builds[: len(spread.long)]
    short_builds = builds[len(spread.long) :]
    anchor_parts = [
        build.ret_local
        for build in builds
        if (build.leg.region or "") not in ASIA_REGIONS
    ]
    anchor = union_calendar(anchor_parts)
    # Calendar is the union after the Asia shift, so a Thursday Tokyo return occupies Wednesday.
    shifted_for_calendar: list[pd.Series] = []
    for build in builds:
        series = build.ret_local
        if spread.alignment == "asia_to_us" and (build.leg.region or "") in ASIA_REGIONS and len(anchor):
            series = shift_asian_returns_to_prior_anchor(series, anchor)
        shifted_for_calendar.append(series)
    calendar = union_calendar(shifted_for_calendar + anchor_parts)
    long_local, long_usd, long_bases = _prepare_side(
        long_builds, which="long", alignment=spread.alignment, anchor=anchor,
        ffill_limit=settings.ffill_limit, calendar=calendar,
    )
    short_local, short_usd, short_bases = _prepare_side(
        short_builds, which="short", alignment=spread.alignment, anchor=anchor,
        ffill_limit=settings.ffill_limit, calendar=calendar,
    )
    frame = pd.DataFrame(
        {
            "long_ret_local": long_local,
            "short_ret_local": short_local,
            "long_ret_usd": long_usd,
            "short_ret_usd": short_usd,
        }
    ).sort_index()
    warning = mixed_basis(long_bases + short_bases)
    instrument_sides = {build.leg.instrument for build in builds}
    if len(instrument_sides) > 1:
        extra = "instrument_mismatch: " + ", ".join(sorted(instrument_sides))
        warning = extra if warning is None else f"{warning}; {extra}"
    return frame, builds, warning
