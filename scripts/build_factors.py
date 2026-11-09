"""Regress each sized spread on the cached factor changes.

Reads cache only. Does not call Bloomberg. Writes the daily beta-neutral,
notional, and vol-neutral sensitivities, a latest-value table, the comparison
with the placeholder driver signs, and a chart per spread.

The beta on a date includes that date. It is a description of co-movement,
not a position.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from strategy_library.config import Factor, Spread, load_factors, load_settings, load_spreads, project_path  # noqa: E402
from strategy_library.data.cache import ParquetCache  # noqa: E402
from strategy_library.factors.changes import build_factor_changes  # noqa: E402
from strategy_library.factors.regress import (  # noqa: E402
    column_name,
    comparison_book,
    factor_timing,
    hypothesis_status,
    rolling_ols,
    sign_flip_halves,
    sign_flip_windows,
)

SIZING = ("notional", "beta", "vol")
BOOKS = ("local", "usd")
NOTABLE_T = 1.96


class _DiskOnly:
    """Satisfies the cache constructor. This script must not fill gaps from Bloomberg."""

    request_count = 0

    def hist(self, *args, **kwargs):
        raise RuntimeError("factor build reads the cache only")


def _levels(cache: ParquetCache, factors: tuple[Factor, ...]) -> dict[str, pd.Series]:
    levels: dict[str, pd.Series] = {}
    missing: list[str] = []
    for factor in factors:
        if not factor.ticker or factor.ticker in levels:
            continue
        frame = cache.read_stored(factor.ticker, "PX_LAST")
        if frame.empty:
            missing.append(factor.ticker)
            continue
        series = pd.Series(frame["value"].to_numpy(), index=pd.to_datetime(frame["date"]), name=factor.ticker)
        series.index = series.index.tz_localize(None) if series.index.tz is not None else series.index
        levels[factor.ticker] = series.sort_index()
    if missing:
        raise RuntimeError("factor cache is missing: " + ", ".join(missing))
    return levels


def _last(series: pd.Series) -> float:
    clean = series.dropna()
    if clean.empty:
        return float("nan")
    return float(clean.iloc[-1])


def _shared_tail(frame: pd.DataFrame) -> pd.Series | None:
    both = frame.dropna()
    if both.empty:
        return None
    return both.iloc[-1]


def _plot_drivers(
    spread: Spread,
    book: str,
    flag: str,
    fit: pd.DataFrame,
    windows: tuple[int, ...],
    path: Path,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    drivers = [factor for factor in spread.expected_drivers if column_name("beta", book, factor, max(windows), "beta") in fit.columns]
    if not drivers:
        return
    short_w, long_w = min(windows), max(windows)
    fig, axes = plt.subplots(len(drivers), 1, figsize=(10, 2.8 * len(drivers)), sharex=True, squeeze=False)
    for ax, factor in zip(axes[:, 0], drivers):
        long_beta = fit[column_name("beta", book, factor, long_w, "beta")]
        short_beta = fit[column_name("beta", book, factor, short_w, "beta")]
        ax.plot(long_beta.index, long_beta, color="black", lw=1.1, label=f"{long_w}d beta")
        ax.plot(short_beta.index, short_beta, color="tab:blue", lw=0.8, alpha=0.85, label=f"{short_w}d beta")
        ax.axhline(0, color="0.5", lw=0.6)
        ax.set_ylabel(f"{factor} beta")
        ax.legend(loc="upper right", fontsize=8)
    title = f"{spread.name} — beta-neutral {book}"
    if "net_vs_gross" in flag:
        title += " — net vs gross"
    fig.suptitle(title)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=100)
    plt.close(fig)


def _plot_heatmap(tstats: pd.DataFrame, path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if tstats.empty:
        return
    fig, ax = plt.subplots(figsize=(12, 10))
    image = ax.imshow(tstats.to_numpy(dtype=float), cmap="RdBu_r", vmin=-4, vmax=4, aspect="auto")
    ax.set_xticks(range(len(tstats.columns)))
    ax.set_xticklabels(list(tstats.columns), rotation=45, ha="right")
    ax.set_yticks(range(len(tstats.index)))
    ax.set_yticklabels(list(tstats.index))
    ax.set_xlabel("Factor")
    ax.set_ylabel("Spread")
    ax.set_title("252-day t-stat, beta-neutral, comparison book")
    fig.colorbar(image, ax=ax, label="t-stat")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=100)
    plt.close(fig)


def _flag_text(value) -> str:
    if value is None or (isinstance(value, float) and not np.isfinite(value)):
        return "same basis"
    text = str(value).strip()
    if text in {"", "nan"}:
        return "same basis"
    return text


def _write_report(latest: pd.DataFrame, hypotheses: pd.DataFrame, path: Path) -> None:
    lines = [
        "# Factor sensitivity",
        "",
        "Betas are from a rolling regression with an intercept. The fit on a date includes that date.",
        "Yield betas are spread return per 1 percentage point, not per basis point.",
        "The driver signs in the config are still placeholders. A disagree below is a disagree with that placeholder.",
        "A native Asian spread is joined on the same calendar date, so a US factor can print after that equity close.",
        "`net_vs_gross` is copied from the sized series and is not a reason to drop the spread.",
        "",
        "## Placeholder signs, beta-neutral, longest window",
        "",
    ]
    if hypotheses.empty:
        lines.append("No hypotheses were configured.")
    else:
        for status in ("disagrees", "matches", "no_estimate"):
            part = hypotheses[hypotheses["hypothesis"] == status]
            lines.append(f"### {status} ({len(part)})")
            lines.append("")
            if part.empty:
                lines.append("None.")
                lines.append("")
                continue
            for row in part.itertuples(index=False):
                beta_txt = "n/a" if not np.isfinite(row.beta) else f"{row.beta:.3f}"
                t_txt = "n/a" if not np.isfinite(row.tstat) else f"{row.tstat:.2f}"
                notable = "notable" if np.isfinite(row.tstat) and abs(row.tstat) >= NOTABLE_T else "not notable"
                timing = ""
                if row.factor_timing == "same_calendar_date_native_asia":
                    timing = " Native Asian close, same calendar date as the US factor."
                lines.append(
                    f"- `{row.spread}` vs `{row.factor}` ({row.book}): "
                    f"beta {beta_txt}, t {t_txt} ({notable}), "
                    f"placeholder {row.placeholder}. {_flag_text(row.basis_flag)}.{timing}"
                )
            lines.append("")
    flips = latest[
        (latest["sizing"] == "beta")
        & (latest["is_comparison_book"])
        & (latest["window"] == latest["window"].max())
        & (latest["sign_flip_windows"])
        & (latest["notable_window_flip"])
    ]
    lines.append("## Short window and long window disagree, and both t-stats are past 1.96")
    lines.append("")
    if flips.empty:
        lines.append("None on the beta-neutral comparison book.")
    else:
            for row in flips.itertuples(index=False):
                beta_txt = "n/a" if not np.isfinite(row.beta) else f"{row.beta:.3f}"
                t_txt = "n/a" if not np.isfinite(row.tstat) else f"{row.tstat:.2f}"
                lines.append(
                    f"- `{row.spread}` vs `{row.factor}` ({row.book}): "
                    f"long beta {beta_txt}, t {t_txt}. {_flag_text(row.basis_flag)}"
                )
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    log = logging.getLogger("build_factors")
    settings = load_settings()
    factors = load_factors()
    spreads = load_spreads()
    windows = settings.factor_windows
    if len(windows) < 2:
        raise RuntimeError("factor_windows needs a short window and a long window")
    short_w, long_w = min(windows), max(windows)
    cache = ParquetCache(project_path(settings.cache_dir), _DiskOnly())
    changes = build_factor_changes(_levels(cache, factors), factors)
    factor_dir = project_path(settings.cache_dir) / "factors"
    factor_dir.mkdir(parents=True, exist_ok=True)
    changes.to_parquet(factor_dir / "changes.parquet")
    log.info("factor changes %s to %s, columns=%s", changes.index.min().date(), changes.index.max().date(), list(changes.columns))

    beta_dir = factor_dir / "betas"
    beta_dir.mkdir(parents=True, exist_ok=True)
    chart_dir = project_path("reports") / "charts"
    latest_rows: list[dict] = []
    hypothesis_rows: list[dict] = []
    heatmap: dict[str, dict[str, float]] = {}

    for spread in spreads:
        sized_path = project_path(settings.cache_dir) / "sized" / f"{spread.id}.parquet"
        if not sized_path.exists():
            raise RuntimeError(f"missing sized series for {spread.id}; run scripts/build_sized.py")
        sized = pd.read_parquet(sized_path)
        sized.index = pd.to_datetime(sized.index)
        flag = ""
        if "basis_flag" in sized.columns and len(sized):
            flag = str(sized["basis_flag"].iloc[0] or "")
            if flag == "nan":
                flag = ""
        book_for_sign = comparison_book(spread.currency)
        timing = factor_timing(spread.region, spread.alignment)
        pieces: dict[str, pd.Series] = {}
        for sizing in SIZING:
            for book in BOOKS:
                returns = sized[f"ret_{sizing}_{book}"]
                for factor in changes.columns:
                    factor_change = changes[factor].reindex(returns.index)
                    for window in windows:
                        fit = rolling_ols(returns, factor_change, window)
                        for stat in ("beta", "tstat", "r2"):
                            pieces[column_name(sizing, book, factor, window, stat)] = fit[stat]
        fit_frame = pd.DataFrame(pieces, index=sized.index)
        # Daily files keep the beta-neutral path only. Notional and vol-neutral
        # are in the latest table. Writing all three every day was about 20 MB
        # a spread, and those two can be rebuilt from the sized returns.
        daily_cols = [
            name
            for name in fit_frame.columns
            if name.startswith("beta|") and name.rsplit("|", 1)[-1] in {"beta", "tstat"}
        ]
        fit_frame[daily_cols].astype("float32").to_parquet(beta_dir / f"{spread.id}.parquet", compression="zstd")
        _plot_drivers(spread, book_for_sign, flag, fit_frame, windows, chart_dir / f"{spread.id}_drivers.png")

        heatmap[spread.id + (" *" if "net_vs_gross" in flag else "")] = {}
        for sizing in SIZING:
            for book in BOOKS:
                for factor in changes.columns:
                    short_beta = fit_frame[column_name(sizing, book, factor, short_w, "beta")]
                    long_beta = fit_frame[column_name(sizing, book, factor, long_w, "beta")]
                    short_t = fit_frame[column_name(sizing, book, factor, short_w, "tstat")]
                    long_t = fit_frame[column_name(sizing, book, factor, long_w, "tstat")]
                    tail = _shared_tail(pd.DataFrame({"sb": short_beta, "lb": long_beta, "st": short_t, "lt": long_t}))
                    flips = sign_flip_windows(short_beta, long_beta)
                    halves = sign_flip_halves(long_beta)
                    notable = bool(
                        tail is not None
                        and flips
                        and abs(float(tail["st"])) >= NOTABLE_T
                        and abs(float(tail["lt"])) >= NOTABLE_T
                    )
                    is_comparison = book == book_for_sign
                    for window in windows:
                        beta = _last(fit_frame[column_name(sizing, book, factor, window, "beta")])
                        tstat = _last(fit_frame[column_name(sizing, book, factor, window, "tstat")])
                        r2 = _last(fit_frame[column_name(sizing, book, factor, window, "r2")])
                        latest_rows.append(
                            {
                                "spread": spread.id,
                                "sizing": sizing,
                                "book": book,
                                "is_comparison_book": is_comparison,
                                "factor": factor,
                                "window": window,
                                "beta": beta,
                                "tstat": tstat,
                                "r2": r2,
                                "sign_flip_windows": flips if window == long_w else False,
                                "sign_flip_halves": halves if window == long_w else False,
                                "notable_window_flip": notable if window == long_w else False,
                                "basis_flag": flag,
                                "factor_timing": timing,
                            }
                        )
                        if sizing == "beta" and is_comparison and window == long_w:
                            heatmap[spread.id + (" *" if "net_vs_gross" in flag else "")][factor] = tstat
                    if sizing == "beta" and is_comparison and factor in spread.expected_drivers:
                        beta = _last(long_beta)
                        tstat = _last(long_t)
                        hypothesis_rows.append(
                            {
                                "spread": spread.id,
                                "factor": factor,
                                "book": book,
                                "window": long_w,
                                "placeholder": spread.expected_drivers[factor],
                                "beta": beta,
                                "tstat": tstat,
                                "r2": _last(fit_frame[column_name(sizing, book, factor, long_w, "r2")]),
                                "hypothesis": hypothesis_status(beta, spread.expected_drivers[factor]),
                                "basis_flag": flag,
                                "factor_timing": timing,
                            }
                        )
        log.info("fit %s flag=%s", spread.id, flag or "none")

    latest = pd.DataFrame(latest_rows)
    hypotheses = pd.DataFrame(hypothesis_rows)
    report_dir = project_path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    latest.to_csv(report_dir / "factor_betas_latest.csv", index=False)
    hypotheses.to_csv(report_dir / "factor_hypotheses.csv", index=False)
    _write_report(latest, hypotheses, report_dir / "factor_sensitivity.md")
    _plot_heatmap(pd.DataFrame(heatmap).T, chart_dir / "tstat_252.png")
    counts = hypotheses["hypothesis"].value_counts().to_dict() if not hypotheses.empty else {}
    notable = latest[
        (latest["sizing"] == "beta") & (latest["is_comparison_book"]) & (latest["notable_window_flip"])
    ]
    log.info("hypotheses %s; notable window flips %s", counts, len(notable))
    print(hypotheses.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
