# POWERHOUSE AI V76.3 FINAL LIVE-WIRED
Mobile-first read-only market intelligence workstation. Preserves V74.3 APIs and engines.

## Data truth
- Upstox/provider status and legacy intelligence are wired into V76.3.
- Candle-volume profile and reconstructed flow are explicitly labelled derived/reconstructed.
- True exchange aggressor Bid×Ask footprint is never fabricated; it remains unavailable unless a feed proves it.
- Automatic broker execution is disabled.

## Render
Build: `pip install -r requirements.txt`
Start: `uvicorn v763_app:app --host 0.0.0.0 --port $PORT`
Keep tokens/secrets only in Render environment variables.
