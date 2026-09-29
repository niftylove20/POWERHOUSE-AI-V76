from v63_engine import global_markets_dashboard

m={"upstox_global_markets":{"markets":[
    {"market":"GIFT NIFTY","price":25123.5,"change_pct":0.22,"status":"LIVE","verified":True,"source":"Upstox Global Instruments","provider_latency":"120 Seconds","epoch":9999999999},
    {"market":"DOW JONES","price":45000,"change_pct":0.11,"status":"LIVE","verified":True,"source":"Upstox Global Instruments","epoch":9999999999},
    {"market":"S&P 500","price":None,"change_pct":None,"status":"UNAVAILABLE","verified":False,"source":"Upstox Global Instruments","epoch":9999999999},
]}}
r=global_markets_dashboard(m)
by={x["market"]:x for x in r["markets"]}
assert by["GIFT NIFTY"]["price"]==25123.5
assert "DOW JONES" not in by
assert "DOW FUTURES" not in by
assert "S&P 500" not in by
assert "yield_curve_10y_2y_bps" in r
print("TEST_V68 PASS — working-feed-only global layer, Dow/dead feeds removed")
