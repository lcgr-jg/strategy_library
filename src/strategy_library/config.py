"""Load the YAML the desk edits. Parsing fails loudly on a bad sign or a missing ticker."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

# Package lives at src/strategy_library/config.py, so parents[2] is the project
# root in an editable checkout. site-packages installs are not how this desk runs.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"

VALID_SIGNS = {"+", "-"}
VALID_ALIGNMENTS = {"native", "asia_to_us"}
VALID_SIZING = {"notional_neutral", "beta_neutral", "vol_neutral"}
VALID_TRANSFORMS = {"diff", "pct"}


@dataclass(frozen=True)
class Leg:
    """One index or ETF in a spread.

    ``tr_ticker`` is a separate total-return index. ``tr_field`` is a history
    field on ``ticker`` itself, used only when no dedicated total-return index
    resolved. ``basis`` is set when the price ticker is already a performance
    index (DAX) so a total-return field is not stacked on top of it.
    """

    ticker: str
    tr_ticker: str | None = None
    tr_field: str | None = None
    price_reference: str | None = None
    currency: str | None = None
    region: str | None = None
    instrument: str = "index"
    basis: str | None = None
    weight: float | None = None


@dataclass(frozen=True)
class Spread:
    id: str
    name: str
    long: tuple[Leg, ...]
    short: tuple[Leg, ...]
    region: str
    currency: str
    themes: tuple[str, ...]
    expected_drivers: dict[str, str]
    sizing_default: str
    vol_long: str | None
    vol_short: str | None
    alignment: str
    notes: str = ""

    def legs(self) -> tuple[Leg, ...]:
        return self.long + self.short


@dataclass(frozen=True)
class Settings:
    history_start: str
    history_end: str | None
    on_server: bool
    cache_dir: str
    beta_window: int
    vol_window: int
    beta_lag: int
    vol_lag: int
    sparse_weekday_coverage: float
    min_history_years: float
    ffill_limit: int
    tr_growth_gap: float
    tr_field: str


@dataclass(frozen=True)
class Factor:
    id: str
    name: str
    transform: str
    unit: str
    ticker: str | None = None
    derived: tuple[str, str] | None = None
    note: str = ""


@dataclass(frozen=True)
class FxQuote:
    currency: str
    ticker: str
    usd_per_local: bool
    note: str = ""


def _read_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _as_leg(raw: dict[str, Any], *, default_currency: str | None, default_region: str | None) -> Leg:
    if "ticker" not in raw:
        raise ValueError(f"Leg is missing ticker: {raw}")
    instrument = str(raw.get("instrument", "index"))
    if instrument not in {"index", "etf"}:
        raise ValueError(f"instrument must be index or etf, got {instrument!r}")
    weight = raw.get("weight")
    return Leg(
        ticker=str(raw["ticker"]),
        tr_ticker=raw.get("tr_ticker") or None,
        tr_field=raw.get("tr_field") or None,
        price_reference=raw.get("price_reference") or None,
        currency=str(raw["currency"]) if raw.get("currency") else default_currency,
        region=str(raw["region"]) if raw.get("region") else default_region,
        instrument=instrument,
        basis=raw.get("basis") or None,
        weight=float(weight) if weight is not None else None,
    )


def _as_legs(raw: Any, *, default_currency: str | None, default_region: str | None) -> tuple[Leg, ...]:
    # A single mapping is one leg. A list is an equal-weight basket (cyclicals).
    if isinstance(raw, dict):
        return (_as_leg(raw, default_currency=default_currency, default_region=default_region),)
    if isinstance(raw, list) and raw:
        return tuple(
            _as_leg(item, default_currency=default_currency, default_region=default_region)
            for item in raw
        )
    raise ValueError(f"long/short must be a leg or a non-empty list of legs, got {raw!r}")


def load_settings(path: Path | None = None) -> Settings:
    raw = _read_yaml(path or CONFIG_DIR / "settings.yaml")
    return Settings(
        history_start=str(raw["history_start"]),
        history_end=raw.get("history_end") or None,
        on_server=bool(raw["on_server"]),
        cache_dir=str(raw["cache_dir"]),
        beta_window=int(raw["beta_window"]),
        vol_window=int(raw["vol_window"]),
        beta_lag=int(raw["beta_lag"]),
        vol_lag=int(raw["vol_lag"]),
        sparse_weekday_coverage=float(raw["sparse_weekday_coverage"]),
        min_history_years=float(raw["min_history_years"]),
        ffill_limit=int(raw["ffill_limit"]),
        tr_growth_gap=float(raw["tr_growth_gap"]),
        tr_field=str(raw["tr_field"]),
    )


def load_spreads(path: Path | None = None) -> tuple[Spread, ...]:
    raw = _read_yaml(path or CONFIG_DIR / "spreads.yaml")
    if not isinstance(raw, list) or not raw:
        raise ValueError("spreads.yaml must be a non-empty list")
    spreads: list[Spread] = []
    seen: set[str] = set()
    for item in raw:
        spread_id = str(item["id"])
        if spread_id in seen:
            raise ValueError(f"Duplicate spread id {spread_id}")
        seen.add(spread_id)
        currency = str(item["currency"])
        region = str(item["region"])
        # Mixed-currency spreads still need a currency on each leg.
        default_currency = None if currency == "mixed" else currency
        drivers = dict(item.get("expected_drivers") or {})
        for factor, sign in drivers.items():
            if sign not in VALID_SIGNS:
                raise ValueError(f"{spread_id} driver {factor} sign must be + or -, got {sign!r}")
        alignment = str(item.get("alignment", "native"))
        if alignment not in VALID_ALIGNMENTS:
            raise ValueError(f"{spread_id} alignment {alignment!r} is not supported")
        sizing = str(item["sizing_default"])
        if sizing not in VALID_SIZING:
            raise ValueError(f"{spread_id} sizing_default {sizing!r} is not supported")
        vol = item.get("vol_legs") or {}
        spreads.append(
            Spread(
                id=spread_id,
                name=str(item["name"]),
                long=_as_legs(item["long"], default_currency=default_currency, default_region=region),
                short=_as_legs(item["short"], default_currency=default_currency, default_region=region),
                region=region,
                currency=currency,
                themes=tuple(item.get("themes") or ()),
                expected_drivers=drivers,
                sizing_default=sizing,
                vol_long=vol.get("long") or None,
                vol_short=vol.get("short") or None,
                alignment=alignment,
                notes=str(item.get("notes") or ""),
            )
        )
    return tuple(spreads)


def load_factors(path: Path | None = None) -> tuple[Factor, ...]:
    raw = _read_yaml(path or CONFIG_DIR / "factors.yaml")
    factors: list[Factor] = []
    for item in raw["factors"]:
        transform = str(item["transform"])
        if transform not in VALID_TRANSFORMS:
            raise ValueError(f"Factor {item['id']} transform must be diff or pct")
        derived_raw = item.get("derived")
        derived = tuple(derived_raw) if derived_raw else None
        if derived is not None and len(derived) != 2:
            raise ValueError(f"Factor {item['id']} derived must be [minus_this, from_this]")
        if derived is None and not item.get("ticker"):
            raise ValueError(f"Factor {item['id']} needs a ticker or a derived pair")
        factors.append(
            Factor(
                id=str(item["id"]),
                name=str(item["name"]),
                transform=transform,
                unit=str(item["unit"]),
                ticker=item.get("ticker") or None,
                derived=derived,  # type: ignore[arg-type]
                note=str(item.get("note") or ""),
            )
        )
    return tuple(factors)


def load_fx(path: Path | None = None) -> dict[str, FxQuote]:
    raw = _read_yaml(path or CONFIG_DIR / "fx.yaml")
    quotes: dict[str, FxQuote] = {}
    for currency, item in raw["quotes"].items():
        quotes[str(currency)] = FxQuote(
            currency=str(currency),
            ticker=str(item["ticker"]),
            usd_per_local=bool(item["usd_per_local"]),
            note=str(item.get("note") or ""),
        )
    return quotes


def load_probe_tickers(path: Path | None = None) -> tuple[str, ...]:
    """Tickers we already know may fail. Live-checked every run so a later entitlement shows up."""
    raw = _read_yaml(path or CONFIG_DIR / "probes.yaml")
    return tuple(str(ticker) for ticker in raw["tickers"])


def project_path(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath(*parts)
