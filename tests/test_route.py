"""Only a B-PIPE entitlement failure is sent to the Terminal."""

from __future__ import annotations

from strategy_library.data.bloomberg import BloombergHistorySource


def test_only_not_entitled_is_routed_to_the_terminal() -> None:
    source = BloombergHistorySource(on_server=True)

    def fake(tickers, on_server):
        assert on_server is True
        return {
            "SPX Index": "OK",
            "IBOV Index": "NOT_ENTITLED",
            "VSTOXX Index": "BAD_SEC",
        }

    source._reference_status = fake  # type: ignore[method-assign]
    source.prepare(["SPX Index", "IBOV Index", "VSTOXX Index"])
    assert source.uses_terminal("IBOV Index") is True
    assert source.uses_terminal("SPX Index") is False
    assert source.uses_terminal("VSTOXX Index") is False
    # A second pass must not ask Bloomberg again once the category is known.
    source._reference_status = lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("reclassified"))  # type: ignore[method-assign]
    source.prepare(["IBOV Index"])
