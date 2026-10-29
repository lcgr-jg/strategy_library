"""Local returns versus unhedged USD returns.

Local mode is the FX-hedged approximation: each leg's own-currency percent
return, with no forward points. USD mode converts the index level by spot and
then computes the return, which is the unhedged result.

``hist`` in desk_core cannot set a Bloomberg currency override, and this
library does not open its own blpapi request to add one. Conversion is done
here from the FX series in ``config/fx.yaml``.
"""

from __future__ import annotations

import pandas as pd

from strategy_library.config import FxQuote


def levels_to_usd(levels: pd.Series, fx: pd.Series, quote: FxQuote) -> pd.Series:
    """Convert a local index level into USD using spot.

    FX is forward-filled onto the index dates with a short limit inside the
    caller. Here we only multiply or divide on dates where both exist.
    ``usd_per_local`` is true for EURUSD-style quotes (dollars per one unit of
    local) and false for USDJPY-style quotes (local currency per one dollar).
    """
    joined = pd.concat({"level": levels, "fx": fx}, axis=1).dropna()
    if joined.empty:
        return pd.Series(dtype=float, name=levels.name)
    if quote.usd_per_local:
        out = joined["level"] * joined["fx"]
    else:
        out = joined["level"] / joined["fx"]
    out.name = levels.name
    return out.sort_index()
