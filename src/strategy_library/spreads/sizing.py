"""Three ways to turn a long leg and a short leg into one spread.

Notional-neutral is long minus short. Beta-neutral subtracts a rolling beta
of the long leg on the short leg. Vol-neutral scales each leg by inverse
realised vol. The beta and the vols used on day t are computed through t-1.
Today's return is not allowed to size today's spread.

When the two realised vols are equal, the vol weights are both 1, so the
spread matches notional-neutral. A quieter leg gets a larger weight. The
weights are scaled to average 1 rather than left as raw 1/vol, so the
cumulative index stays in return units.
"""

from __future__ import annotations

import logging

import pandas as pd

from strategy_library.config import Settings

logger = logging.getLogger(__name__)

INDEX_BASE = 100.0


def rolling_beta(long: pd.Series, short: pd.Series, window: int, lag: int) -> pd.Series:
    """Slope of long on short. Lagged so day t does not use day t's return.

    The slope has an intercept: average outperformance stays in the residual
    instead of being forced into the hedge ratio. Covariance and variance both
    use the same /N second moment, so the ratio is the OLS slope.
    """
    paired = pd.concat({"long": long, "short": short}, axis=1)
    roll = paired.rolling(window, min_periods=window)
    mean_long = roll["long"].mean()
    mean_short = roll["short"].mean()
    mean_product = (paired["long"] * paired["short"]).rolling(window, min_periods=window).mean()
    var_short = (paired["short"] ** 2).rolling(window, min_periods=window).mean() - mean_short**2
    # A flat short leg has no hedge ratio. A tiny negative from float error is the same thing.
    var_short = var_short.where(var_short > 1e-18)
    beta = (mean_product - mean_long * mean_short) / var_short
    return beta.shift(lag)


def rolling_vol(returns: pd.Series, window: int, lag: int) -> pd.Series:
    """Sample standard deviation, lagged by the same rule as the beta."""
    return returns.rolling(window, min_periods=window).std(ddof=1).shift(lag)


def _vol_weights(long_vol: pd.Series, short_vol: pd.Series) -> tuple[pd.Series, pd.Series]:
    inv_long = 1.0 / long_vol.where(long_vol > 0)
    inv_short = 1.0 / short_vol.where(short_vol > 0)
    total = inv_long + inv_short
    # 2 / (inv_l + inv_s) * inv_l equals 1 when the vols match.
    weight_long = 2.0 * inv_long / total
    weight_short = 2.0 * inv_short / total
    return weight_long, weight_short


def cumulative_index(returns: pd.Series, base: float = INDEX_BASE) -> pd.Series:
    """Compound simple returns. 100 is the close before the first valid return.

    A missing return is left missing and is not treated as a zero. The next
    valid day compounds from the previous valid level, so a hole does not
    flatten the index and does not drop the later history.
    """
    out = pd.Series(index=returns.index, dtype=float)
    valid = returns.dropna()
    if valid.empty:
        return out
    out.loc[valid.index] = base * (1.0 + valid).cumprod()
    return out


def size_pair(long: pd.Series, short: pd.Series, settings: Settings, suffix: str) -> pd.DataFrame:
    """Size one currency version of the two legs. Column names end with ``suffix``."""
    beta = rolling_beta(long, short, settings.beta_window, settings.beta_lag)
    long_vol = rolling_vol(long, settings.vol_window, settings.vol_lag)
    short_vol = rolling_vol(short, settings.vol_window, settings.vol_lag)
    weight_long, weight_short = _vol_weights(long_vol, short_vol)
    notional = long - short
    beta_neutral = long - beta * short
    vol_neutral = weight_long * long - weight_short * short
    return pd.DataFrame(
        {
            f"ret_notional_{suffix}": notional,
            f"idx_notional_{suffix}": cumulative_index(notional),
            f"ret_beta_{suffix}": beta_neutral,
            f"idx_beta_{suffix}": cumulative_index(beta_neutral),
            f"beta_{suffix}": beta,
            f"ret_vol_{suffix}": vol_neutral,
            f"idx_vol_{suffix}": cumulative_index(vol_neutral),
            f"w_long_vol_{suffix}": weight_long,
            f"w_short_vol_{suffix}": weight_short,
        }
    )


def size_panel(panel: pd.DataFrame, settings: Settings, basis_flag: str = "") -> pd.DataFrame:
    """Add the three spread returns and their cumulative indexes to a leg panel.

    Local and USD are sized separately. A USD beta is not applied to a local return.
    ``basis_flag`` is copied onto every row so a net-versus-gross mix stays attached
    to the series instead of living only in a side report.
    """
    local = size_pair(panel["long_ret_local"], panel["short_ret_local"], settings, "local")
    usd = size_pair(panel["long_ret_usd"], panel["short_ret_usd"], settings, "usd")
    sized = pd.concat([panel, local, usd], axis=1)
    sized["basis_flag"] = basis_flag
    logger.info(
        "sized spread rows=%s notional=%s beta=%s vol=%s flag=%s",
        len(sized),
        int(sized["ret_notional_local"].notna().sum()),
        int(sized["ret_beta_local"].notna().sum()),
        int(sized["ret_vol_local"].notna().sum()),
        basis_flag or "none",
    )
    return sized
