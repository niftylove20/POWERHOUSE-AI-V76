POWERHOUSE AI V74 — FINAL FULL CUMULATIVE PACKAGE

Base: user-supplied POWERHOUSE_AI_V73_LTS_FINAL_FULL_CUMULATIVE(1).zip
Upgrade: V74 Maximum Move Capture / No-Miss Accountability layer
Startup: uvicorn v74_app:app --host 0.0.0.0 --port $PORT

This is a full deployable source tree, not an overlay-only package.
Legacy app.py and V72/V73 engines remain included for compatibility and rollback.
V72.3 full cumulative rollback archive is preserved under _ROLLBACK/.
No .env secrets or broker tokens were added by this merge.

Primary V74 routes are mounted before legacy routes by v74_app.py.
Read-only intelligence policy remains locked; no automatic broker order placement is enabled.
