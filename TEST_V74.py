from v74_engine import MOVE_CLASSES, TOP_LEVEL_TABS, build_v74, hero5_execution_plan, seven_scouts


def _row():
    return {
        "symbol": "TEST",
        "ltp": 1000.0,
        "change_pct": 1.8,
        "volume": 500000,
        "rvol": 2.2,
        "futures_oi_change_pct": 5.0,
        "oi_velocity": 3.0,
        "sector_strength": 78,
        "sector_ignition": True,
        "total_buy_qty": 800000,
        "total_sell_qty": 300000,
        "bid": 999.5,
        "ask": 1000.5,
        "pattern": "BREAKOUT",
        "pattern_quality": 82,
        "breakout": True,
        "premium_response": 76,
        "iv": 18,
        "gamma": 72,
        "v72_side": "CE",
        "pre_move_stage": "ARMING",
        "quote_age_sec": 1,
    }


def main():
    assert len(TOP_LEVEL_TABS) == 35
    assert "MISSED MOVES" in TOP_LEVEL_TABS and "PERFORMANCE" in TOP_LEVEL_TABS
    r = _row()
    scouts = seven_scouts(r)
    assert scouts["ready_count"] >= 6
    assert 0 <= scouts["aggregate_score"] <= 100

    # build_v74 uses the real cumulative V73/V72 pipeline; the synthetic snapshot must
    # remain safe even if some provider-only fields are unavailable.
    out = build_v74({"fno_universe": [r], "stocks": [r], "websocket_connected": True}, record=False)
    assert out["version"] == "74.0"
    assert out["read_only"] is True and out["execution_enabled"] is False
    assert len(out["tabs"]) == 35
    for row in (out.get("radar") or {}).get("candidates") or []:
        assert row.get("move_class") in MOVE_CLASSES
        assert (row.get("data_truth") or {}).get("missing_scouts") is not None
    assert (out.get("coverage") or {}).get("silent_misses_allowed") is False
    print("TEST_V74 PASS")


if __name__ == "__main__":
    main()
