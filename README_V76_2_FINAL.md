# POWERHOUSE AI V76.2 — FINAL MOBILE ORDER FLOW

Additive release built on the locked V74.3 master backend.

## UI lock
Mobile-first dark workstation matching the approved reference: Chart, Order Flow, Profile, Options/Gamma, Dynamite and Replay navigation; Market Profile/TPO, footprint, DOM/depth, CVD/Delta, options/GEX, participation, key levels, news and Dynamite analysis panels.

## Truth policy
The visual shell intentionally shows `—` for order-flow/DOM/OI fields until verified live data is available. It never labels reconstructed or unavailable values as live exchange truth.

## Run
`pip install -r requirements.txt`
`uvicorn v76_app:app --host 0.0.0.0 --port 8000`

Render start command:
`uvicorn v76_app:app --host 0.0.0.0 --port $PORT`

Existing V74.3 APIs and engines are preserved. Broker execution remains disabled/read-only.
