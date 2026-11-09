"""Refresh the spread study and open the interactive factor map.

Default uses the parquet already on disk. Pass --update-history to pull
Bloomberg first (B-PIPE, with Terminal only for NOT_ENTITLED names).

Examples:
  ..\\.venv\\Scripts\\python.exe scripts\\refresh_study.py
  ..\\.venv\\Scripts\\python.exe scripts\\refresh_study.py --update-history
  ..\\.venv\\Scripts\\python.exe scripts\\refresh_study.py --no-open
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def _run(script: str) -> None:
    path = ROOT / "scripts" / script
    logging.info("running %s", path.name)
    subprocess.run([PYTHON, str(path)], cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--update-history",
        action="store_true",
        help="Fetch missing Bloomberg dates before rebuilding sized spreads and factor betas.",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Write reports/factor_map.html without opening a browser.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.update_history:
        _run("verify_tickers.py")
    _run("build_sized.py")
    _run("build_factors.py")
    _run("write_factor_map.py")

    html = ROOT / "reports" / "factor_map.html"
    if not html.exists():
        raise SystemExit(f"expected {html} after write_factor_map")
    logging.info("factor map ready at %s", html)
    if not args.no_open:
        webbrowser.open(html.resolve().as_uri())
    print(html)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
