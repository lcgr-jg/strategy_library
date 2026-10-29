"""Decide whether a leg is price or total return, without mixing the two.

Bloomberg's historical field TOT_RETURN_INDEX_GROSS_DVDS compounds dividends on
a price index (it tracks SPTR, not SPX, over long windows). On a performance
index such as DAX the same field must not be applied again. The growth gap
between the price series and the candidate total-return series is what decides.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

BASIS_PRICE = "price"
BASIS_TOTAL_RETURN = "total_return"
BASIS_TOTAL_RETURN_GROSS = "total_return_gross"
BASIS_TOTAL_RETURN_NET = "total_return_net"
BASIS_ETF = "etf_price"


@dataclass(frozen=True)
class SeriesChoice:
    levels: pd.Series
    basis: str
    source: str
    note: str


def growth_ratio(levels: pd.Series) -> float | None:
    """Last / first on overlapping non-null points. None if the series cannot grow."""
    clean = levels.dropna().sort_index()
    if len(clean) < 2:
        return None
    first = float(clean.iloc[0])
    last = float(clean.iloc[-1])
    if first == 0:
        return None
    return last / first


def adds_total_return(price: pd.Series, candidate: pd.Series, *, gap: float) -> bool:
    """True when the candidate compounded meaningfully more than the price series.

    The comparison is on the overlapping date range so a shorter total-return
    history is not punished for missing the early years. ``gap`` is a relative
    difference in growth multiples (0.05 means 5%). Dividends over a multi-year
    sample clear that bar; a one-day field glitch does not.
    """
    joined = pd.concat({"price": price, "candidate": candidate}, axis=1).dropna()
    if len(joined) < 2:
        return False
    price_growth = growth_ratio(joined["price"])
    candidate_growth = growth_ratio(joined["candidate"])
    if price_growth is None or candidate_growth is None or price_growth == 0:
        return False
    return (candidate_growth / price_growth) - 1.0 > gap


def choose_levels(
    *,
    price: pd.Series,
    total_return: pd.Series | None,
    configured_basis: str | None,
    gap: float,
    source_label: str,
    dedicated: bool = False,
    price_is_already_total_return: bool = False,
) -> SeriesChoice:
    """Pick the series the spread will actually use.

    ``dedicated`` means the config named a separate total-return index (SPTR).
    That series is used whenever it has data. A basis label on that leg describes
    the total-return index, not the price ticker.

    ``price_is_already_total_return`` is the other case: DAX, where the price
    ticker is the performance index. A field that compounds further is not
    stacked on top of it.
    """
    price = price.dropna().sort_index()
    candidate = None if total_return is None else total_return.dropna().sort_index()

    if dedicated:
        if candidate is None or candidate.empty:
            return SeriesChoice(
                price,
                configured_basis or BASIS_PRICE,
                "price",
                "dedicated total-return ticker was empty; using the price ticker",
            )
        note = "dedicated total-return ticker"
        if not adds_total_return(price, candidate, gap=gap):
            note += "; growth does not exceed the price ticker over the overlap"
        return SeriesChoice(candidate, configured_basis or BASIS_TOTAL_RETURN, source_label, note)

    if candidate is None or candidate.empty:
        basis = configured_basis or BASIS_PRICE
        note = "price ticker is already a total-return index" if price_is_already_total_return else "no total-return series; using the price ticker"
        return SeriesChoice(price, basis, "price", note)

    compounds = adds_total_return(price, candidate, gap=gap)
    if price_is_already_total_return:
        if compounds:
            return SeriesChoice(
                price,
                configured_basis or BASIS_TOTAL_RETURN,
                "price",
                "total-return candidate compounds more than this performance index; not stacked",
            )
        return SeriesChoice(
            price,
            configured_basis or BASIS_TOTAL_RETURN,
            "price",
            "price ticker matches the total-return candidate; using the price ticker",
        )
    if compounds:
        # The only field this library requests is the gross-dividend history field.
        basis = configured_basis or BASIS_TOTAL_RETURN_GROSS
        return SeriesChoice(candidate, basis, source_label, "using total return; it compounds more than price")
    basis = configured_basis or BASIS_PRICE
    return SeriesChoice(price, basis, "price", "total-return candidate did not compound beyond price")


def mixed_basis(labels: list[str]) -> str | None:
    """Return a warning when the two sides of a spread are not on the same basis."""
    present = {label for label in labels if label}
    if len(present) <= 1:
        return None
    return "mixed_basis: " + ", ".join(sorted(present))
