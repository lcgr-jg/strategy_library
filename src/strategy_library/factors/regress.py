"""Rolling univariate regression of a spread return on a factor change.

The beta stamped on day t uses the window that ends on day t, including day t.
That is the sensitivity of the two series together. It is not a weight and it
is not lagged. Sizing weights live in spreads.sizing and those are lagged.

The window is a count of sessions where both the spread and the factor printed.
A holiday that removed one of them is dropped before the roll, so it does not
punch a missing value through the next 252 days.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# A short-window sign that disagrees with the long-window sign is a regime
# difference, not a data error. The halves flag is the same idea through time:
# the median of the early long-window betas against the median of the later ones.
# A 20% day-count would mark ordinary noise.


def column_name(sizing: str, book: str, factor: str, window: int, stat: str) -> str:
    return f"{sizing}|{book}|{factor}|{window}|{stat}"


def comparison_book(currency: str) -> str:
    """Local when the spread has one currency. USD when the legs do not share one.

    A mixed spread has no single local return to put next to a hypothesis.
    """
    return "usd" if currency == "mixed" else "local"


def factor_timing(region: str, alignment: str) -> str:
    """Same calendar date for every spread.

    An Asia-to-US spread already carries the Asian return on the prior US date.
    A native Asian spread does not, so a US factor that prints after the Asian
    close is paired with an equity return that could not have seen it.
    """
    if alignment == "native" and region in {"JP", "HK", "AU"}:
        return "same_calendar_date_native_asia"
    return "same_calendar_date"


def rolling_ols(y: pd.Series, x: pd.Series, window: int) -> pd.DataFrame:
    """OLS slope of y on x with an intercept, plus its t-stat and R².

    The intercept keeps a constant drift out of the slope. R² is the squared
    correlation, which is the univariate identity. The t-stat uses n−2 so a
    window shorter than 3 sessions is not a regression.
    """
    empty = pd.DataFrame(index=y.index, columns=["beta", "tstat", "r2"], dtype=float)
    if window < 3:
        raise ValueError(f"window must be at least 3, got {window}")
    paired = pd.concat({"y": y, "x": x}, axis=1).dropna()
    if len(paired) < window:
        return empty
    yy = paired["y"]
    xx = paired["x"]
    n = float(window)
    mean_y = yy.rolling(window, min_periods=window).mean()
    mean_x = xx.rolling(window, min_periods=window).mean()
    var_y = (yy * yy).rolling(window, min_periods=window).mean() - mean_y**2
    var_x = (xx * xx).rolling(window, min_periods=window).mean() - mean_x**2
    cov = (yy * xx).rolling(window, min_periods=window).mean() - mean_y * mean_x
    var_x_safe = var_x.where(var_x > 1e-18)
    var_y_safe = var_y.where(var_y > 1e-18)
    beta = cov / var_x_safe
    # Sum of squares equals n times the /n second moment.
    sxx = n * var_x
    sst = n * var_y
    sse = (sst - (beta**2) * sxx).clip(lower=0)
    se = np.sqrt((sse / (n - 2.0)) / sxx.where(sxx > 0))
    tstat = beta / se.replace(0, np.nan)
    r2 = (cov**2) / (var_x_safe * var_y_safe)
    out = pd.DataFrame({"beta": beta, "tstat": tstat, "r2": r2.clip(lower=0, upper=1)})
    return out.reindex(y.index)


def _last_shared(left: pd.Series, right: pd.Series) -> tuple[float, float]:
    both = pd.concat({"left": left, "right": right}, axis=1).dropna()
    if both.empty:
        return (np.nan, np.nan)
    return float(both["left"].iloc[-1]), float(both["right"].iloc[-1])


def sign_flip_windows(short: pd.Series, long: pd.Series) -> bool:
    """True when the latest short-window beta and long-window beta have opposite signs."""
    a, b = _last_shared(short, long)
    if not np.isfinite(a) or not np.isfinite(b) or a == 0 or b == 0:
        return False
    return (a > 0) != (b > 0)


def sign_flip_halves(beta: pd.Series) -> bool:
    """True when the early half and the later half of a beta path have opposite median signs."""
    clean = beta.dropna()
    if len(clean) < 2:
        return False
    mid = len(clean) // 2
    early = float(clean.iloc[:mid].median())
    late = float(clean.iloc[mid:].median())
    if early == 0 or late == 0 or not np.isfinite(early) or not np.isfinite(late):
        return False
    return (early > 0) != (late > 0)


def hypothesis_status(beta: float, sign: str) -> str:
    """Compare a point estimate with the + or − written in the spread config.

    Those signs are placeholders until the desk edits them. A disagree here is
    a disagree with that placeholder, not with a measured view.
    """
    if sign not in {"+", "-"}:
        raise ValueError(f"sign must be + or -, got {sign!r}")
    if not np.isfinite(beta) or beta == 0:
        return "no_estimate"
    got = "+" if beta > 0 else "-"
    return "matches" if got == sign else "disagrees"
