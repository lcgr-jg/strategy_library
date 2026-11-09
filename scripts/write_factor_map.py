"""Write the interactive factor map HTML from the cached study outputs.

Does not call Bloomberg. Run after build_sized and build_factors, or through
scripts/refresh_study.py.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from strategy_library.config import load_factors, load_settings, load_spreads, project_path  # noqa: E402
from strategy_library.reports.factor_map import FactorMapPaths, build_factor_map_payload, write_factor_map  # noqa: E402


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    settings = load_settings()
    windows = settings.factor_windows
    paths = FactorMapPaths(
        sized_dir=project_path(settings.cache_dir) / "sized",
        beta_dir=project_path(settings.cache_dir) / "factors" / "betas",
        latest_csv=project_path("reports") / "factor_betas_latest.csv",
    )
    payload = build_factor_map_payload(
        load_spreads(),
        load_factors(),
        paths,
        short_window=min(windows),
        long_window=max(windows),
    )
    out = write_factor_map(payload, project_path("reports") / "factor_map.html")
    size_mb = out.stat().st_size / (1024 * 1024)
    logging.info("wrote %s (%.1f MB, as_of=%s)", out, size_mb, payload.get("as_of"))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
