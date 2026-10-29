"""Total-return choice and USD conversion. Synthetic levels only."""

from __future__ import annotations

import pandas as pd

from strategy_library.config import FxQuote, Leg, Settings, load_factors, load_fx, load_spreads
from strategy_library.data.basis import adds_total_return, choose_levels, mixed_basis
from strategy_library.data.fx import levels_to_usd
from strategy_library.data.panel import LevelStore, build_spread_frame


def _series(values: list[float]) -> pd.Series:
    idx = pd.bdate_range("2020-01-01", periods=len(values))
    return pd.Series(values, index=idx)


def test_field_that_compounds_more_than_price_is_total_return() -> None:
    price = _series([100, 100, 110])
    total = _series([100, 101, 130])
    assert adds_total_return(price, total, gap=0.05)
    choice = choose_levels(price=price, total_return=total, configured_basis=None, gap=0.05, source_label="field")
    assert choice.source == "field"
    assert choice.basis == "total_return_gross"
    assert float(choice.levels.iloc[-1]) == 130


def test_dedicated_total_return_ticker_is_used_even_when_basis_is_labelled() -> None:
    # basis=total_return_gross here describes SPTR, not "SPX is already total return".
    price = _series([100, 110, 120])
    total = _series([100, 112, 140])
    choice = choose_levels(
        price=price,
        total_return=total,
        configured_basis="total_return_gross",
        gap=0.05,
        source_label="SPTR Index",
        dedicated=True,
    )
    assert choice.source == "SPTR Index"
    assert float(choice.levels.iloc[-1]) == 140


def test_performance_index_is_not_stacked() -> None:
    # DAX-style: the candidate compounds further, and the ticker is already total return.
    price = _series([100, 110, 150])
    stacked = _series([100, 112, 180])
    choice = choose_levels(
        price=price,
        total_return=stacked,
        configured_basis="total_return",
        gap=0.05,
        source_label="field",
        price_is_already_total_return=True,
    )
    assert choice.source == "price"
    assert "not stacked" in choice.note
    assert float(choice.levels.iloc[-1]) == 150


def test_usd_conversion_respects_quote_direction() -> None:
    levels = _series([100, 100])
    fx = _series([150.0, 150.0])
    jpy = FxQuote("JPY", "USDJPY Curncy", usd_per_local=False)
    eur = FxQuote("EUR", "EURUSD Curncy", usd_per_local=True)
    assert abs(float(levels_to_usd(levels, fx, jpy).iloc[-1]) - (100 / 150)) < 1e-12
    assert abs(float(levels_to_usd(levels, _series([1.2, 1.2]), eur).iloc[-1]) - 120) < 1e-12


def test_mixed_basis_and_basket_requires_every_sleeve() -> None:
    assert mixed_basis(["total_return_net", "total_return"]) is not None
    assert mixed_basis(["total_return_gross", "total_return_gross"]) is None

    class Store(LevelStore):
        def levels(self, ticker: str, field: str, start: str, end: str) -> pd.Series:
            # Materials stop printing. The hole is longer than ffill_limit, so the
            # last day must stay missing instead of handing the whole basket to industrials.
            idx = pd.bdate_range("2020-01-01", periods=6)
            data = {
                "S5INDU Index": [100, 110, 110, 110, 110, 121],
                "S5MATR Index": [100, 100, None, None, None, None],
                "S5CONS Index": [100, 100, 100, 100, 100, 100],
                "S5UTIL Index": [100, 100, 100, 100, 100, 100],
            }
            return pd.Series(data[ticker], index=idx, dtype=float)

    spread = next(item for item in load_spreads() if item.id == "us_cyc_def")
    settings = Settings(
        history_start="2020-01-01",
        history_end="2020-02-01",
        on_server=True,
        cache_dir="cache",
        beta_window=252,
        vol_window=63,
        beta_lag=1,
        vol_lag=1,
        sparse_weekday_coverage=0.8,
        min_history_years=5,
        ffill_limit=1,
        tr_growth_gap=0.05,
        tr_field="TOT_RETURN_INDEX_GROSS_DVDS",
    )
    # Force the store to ignore the total-return field by giving price only.
    # build_leg asks for the field too; return the same path so it does not look like extra dividends.
    original = Store.levels

    def levels(self, ticker, field, start, end):
        return original(self, ticker, "PX_LAST", start, end)

    Store.levels = levels  # type: ignore[method-assign]
    frame, _, warning = build_spread_frame(
        spread, Store(), settings, load_fx(), {}, start="2020-01-01", end="2020-02-01"
    )
    assert warning is None
    # The materials hole is past the one-session bridge, so industrials must not become the whole basket.
    assert pd.isna(frame["long_ret_local"].iloc[-1])


def test_asia_shift_is_applied_to_the_configured_spread() -> None:
    class Store(LevelStore):
        def levels(self, ticker: str, field: str, start: str, end: str) -> pd.Series:
            idx = pd.to_datetime(["2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11"])
            if ticker == "HSCEI Index":
                # Flat, then +10% on Thursday. That Thursday move belongs on Wednesday.
                return pd.Series([100.0, 100.0, 100.0, 110.0], index=idx)
            if ticker == "SPTR Index":
                return pd.Series([100.0, 100.0, 100.0, 100.0], index=idx)
            if ticker == "SPX Index":
                return pd.Series([50.0, 50.0, 50.0, 50.0], index=idx)
            if ticker == "USDHKD Curncy":
                return pd.Series([7.8, 7.8, 7.8, 7.8], index=idx)
            raise KeyError(ticker)

    spread = next(item for item in load_spreads() if item.id == "hscei_spx")
    settings = Settings(
        history_start="2024-01-08",
        history_end="2024-01-11",
        on_server=True,
        cache_dir="cache",
        beta_window=252,
        vol_window=63,
        beta_lag=1,
        vol_lag=1,
        sparse_weekday_coverage=0.8,
        min_history_years=5,
        ffill_limit=5,
        tr_growth_gap=0.5,
        tr_field="TOT_RETURN_INDEX_GROSS_DVDS",
    )
    # gap 0.5 forces the identical price and tr_field path to stay on price for HSCEI,
    # and SPTR is flat versus SPX so the short leg stays on the configured total-return ticker
    # only if it compounds. SPTR is flat and SPX is flat, so growth gap is 0 and SPTR is rejected.
    # Give SPX a lower growth by making the price path fall... simpler to set SPX price much lower growth.
    frame, builds, _ = build_spread_frame(
        spread, Store(), settings, load_fx(), {"USDHKD Curncy": Store().levels("USDHKD Curncy", "PX_LAST", "", "")},
        start="2024-01-08",
        end="2024-01-11",
    )
    thursday = pd.Timestamp("2024-01-11")
    wednesday = pd.Timestamp("2024-01-10")
    # Thursday's +10% Hong Kong move is stamped on Wednesday, and Thursday itself is a zero
    # only if some other leg trades Thursday. SPX is flat so it has a 0 return on Thursday
    # after the first day. The Hong Kong +10% must not sit on Thursday.
    assert abs(frame.loc[wednesday, "long_ret_local"] - 0.10) < 1e-12
    assert frame.loc[thursday, "long_ret_local"] == 0.0
    assert all(build.leg.ticker != "missing" for build in builds)


def test_config_files_load() -> None:
    spreads = load_spreads()
    assert {item.id for item in spreads} >= {"tpx_nky", "us_cyc_def", "ibov_mxef", "kre_s5finl", "krx_s5finl"}
    factors = {item.id: item for item in load_factors()}
    assert factors["us_2s10s"].derived == ("us_10y", "us_2y")
    assert factors["us_10y"].transform == "diff"
    assert factors["dxy"].transform == "pct"
    assert load_fx()["JPY"].usd_per_local is False
    assert load_fx()["EUR"].usd_per_local is True
    tpx = next(item for item in spreads if item.id == "tpx_nky")
    assert tpx.alignment == "native"
    assert tpx.expected_drivers["jgb_10y"] == "+"
    hscei = next(item for item in spreads if item.id == "hscei_spx")
    assert hscei.alignment == "asia_to_us"
    assert isinstance(next(item for item in spreads if item.id == "us_cyc_def").long, tuple)
