# Equity index spread library

Maps macro shocks to equity index spreads. Phase 1 is the config and the data layer.
Sizing, factor regressions, event studies and the volatility book are not built yet.

`desk_core` is the Bloomberg client. This project wraps `refdata.hist` and `refdata.live`.
It does not open its own `blpapi` session and it does not change `desk_core`.

## Install

Use the Coding virtualenv, which already has `desk_core` and Bloomberg:

```powershell
cd strategy_library
..\.venv\Scripts\python.exe -m pip install -e ".[dev]"
..\.venv\Scripts\python.exe -m pytest tests -q
..\.venv\Scripts\python.exe scripts\verify_tickers.py
```

History requests go to B-PIPE (`on_server: true` in `config/settings.yaml`).
Credentials stay in `desk_core/login.py`. Nothing in this repo reads or stores them.

## What is in the config

- `config/spreads.yaml` defines each spread. A `long` or `short` value can be one leg or a list. A list is an equal-weight basket, and a day is dropped unless every sleeve printed or was bridged across a short holiday.
- `tr_ticker` is a dedicated total-return index. `tr_field` is the historical field `TOT_RETURN_INDEX_GROSS_DVDS` on the price ticker, used only when no dedicated total-return index resolved. On a price index that field compounds like a total-return index. It is not applied on top of an index that is already a performance index (DAX, and MDAX as named by Bloomberg).
- `basis: total_return` means the price ticker itself is the total-return series.
- `expected_drivers` are hypotheses. They are not measured betas.
- `config/factors.yaml` records the transform for each macro factor. Yields are daily changes in percentage points, not basis points. Prices (DXY, oil, copper, USDJPY) are simple percent changes. The 2s10s slope is the 10y yield minus the 2y yield, then the daily change of that slope.
- `config/fx.yaml` is the spot quote used for the unhedged USD series. EURUSD is multiplied. USDJPY is divided. Local mode does not use FX: it is each leg's own-currency return, and it ignores forward points.
- `config/events.yaml` is where FOMC, ECB, BoJ and BoE dates go. CPI and NFP tickers are listed there for a later surprise calculation.
- `config/probes.yaml` is the list of symbols that failed, or that are alternates (net versus gross). They are snapshot-checked on every verification run.

## Cache

One parquet per ticker and field, under `cache/`. A rerun fetches only the dates outside the stored range. The manifest remembers an empty tail, such as a holiday, so that gap is not requested again. A ticker that has never returned a row is not written, so a permission failure is retried next time.

Requests are one ticker and one field. `desk_core.refdata.hist` aborts the whole call if one security errors while it is reading field data, so a batch would drop the later names. Reference snapshots are batched, because an unknown security comes back empty instead of raising. Every history and snapshot call is logged with a running count.

B-PIPE is the default session. Before history is requested, one reference call reads Bloomberg's security error, which `refdata.live` does not keep. A ticker that comes back `NOT_ENTITLED` on the commodities B-PIPE application is then pulled from the desktop Terminal. An invalid ticker is not retried there. Entitled names stay on B-PIPE. The two sessions are a singleton inside `desk_core`, so the verification run asks for every B-PIPE series before it opens the Terminal.

## Calendar

Each leg's return is computed on the days that leg traded. On the spread calendar, a day the leg was shut is a zero return, for at most `ffill_limit` spread sessions (default 5). A longer hole stays missing.

`alignment: asia_to_us` is set on HSCEI versus SPX and ASX 200 versus SPX. Hong Kong and Sydney are already closed before the US cash open. The Asian session that can react to Wednesday's US news is Thursday. That Thursday return is placed on Wednesday's US date: the Asian print dated D goes on the last US session strictly before D. Two Asian sessions that fall across a US holiday are compounded onto that one US date.

Japan versus Japan stays on `native`. MSCI EM stays on `native` as well. That index is struck around the US close and already contains the same day's Asian sessions, so shifting it would move Asia twice. A later event study can still shift a native Asian spread explicitly.

## Verification

`scripts/verify_tickers.py` writes `reports/ticker_verification.md` and the csv files next to it. A series shorter than five years, or covering less than 80% of weekdays between its first and last print, is flagged and kept. Weekdays are the denominator, so Christmas is not a hole.

The report is the list of what failed. Spreads are not dropped because a ticker failed.
