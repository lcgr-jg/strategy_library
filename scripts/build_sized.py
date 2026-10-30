"""Build the three sized spread indexes from the cached leg panels.

Reads cache/panels and the basis column already written by the verification
report. Does not call Bloomberg. A net leg against a gross or performance leg
is marked net_vs_gross on the series itself.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from strategy_library.config import load_settings, project_path  # noqa: E402
from strategy_library.data.basis import net_vs_gross  # noqa: E402
from strategy_library.spreads.sizing import size_panel  # noqa: E402


def _labels(bases: str) -> list[str]:
    labels: list[str] = []
    for part in str(bases).split(","):
        if "=" not in part:
            continue
        labels.append(part.split("=", 1)[1].split("/", 1)[0].strip())
    return labels


def _flag(bases: str, warning: str) -> str:
    parts = [piece.strip() for piece in str(warning).split(";") if piece and piece.strip() and piece.strip() != "nan"]
    extra = net_vs_gross(_labels(bases))
    if extra and extra not in parts:
        parts.append(extra)
    return "; ".join(parts)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    settings = load_settings()
    panel_dir = project_path(settings.cache_dir) / "panels"
    out_dir = project_path(settings.cache_dir) / "sized"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = project_path("reports") / "spread_verification.csv"
    report = pd.read_csv(report_path) if report_path.exists() else pd.DataFrame()
    by_id = report.set_index("id") if not report.empty and "id" in report.columns else pd.DataFrame()

    rows: list[dict] = []
    for path in sorted(panel_dir.glob("*.parquet")):
        panel = pd.read_parquet(path)
        panel.index = pd.to_datetime(panel.index)
        bases = ""
        warning = ""
        if path.stem in by_id.index:
            bases = str(by_id.at[path.stem, "bases"]) if "bases" in by_id.columns else ""
            warning = str(by_id.at[path.stem, "warning"]) if "warning" in by_id.columns else ""
        flag = _flag(bases, warning)
        sized = size_panel(panel, settings, flag)
        sized.to_parquet(out_dir / path.name)
        rows.append(
            {
                "id": path.stem,
                "basis_flag": flag,
                "net_vs_gross": "net_vs_gross" in flag,
                "n_notional": int(sized["ret_notional_local"].notna().sum()),
                "n_beta": int(sized["ret_beta_local"].notna().sum()),
                "n_vol": int(sized["ret_vol_local"].notna().sum()),
                "first_beta": ""
                if sized["ret_beta_local"].dropna().empty
                else sized["ret_beta_local"].dropna().index[0].strftime("%Y-%m-%d"),
                "first_vol": ""
                if sized["ret_vol_local"].dropna().empty
                else sized["ret_vol_local"].dropna().index[0].strftime("%Y-%m-%d"),
            }
        )
    summary = pd.DataFrame(rows)
    project_path("reports").mkdir(parents=True, exist_ok=True)
    summary.to_csv(project_path("reports") / "sized_spreads.csv", index=False)
    logging.info("wrote %s sized spreads", len(summary))
    print(summary.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
