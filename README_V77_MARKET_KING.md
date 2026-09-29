# POWERHOUSE AI V77 — MARKET KING
Cumulative additive build over the supplied V76.3 205-file master. V74.3 locked backend/API lineage remains preserved.

## Start
`pip install -r requirements.txt`
`uvicorn v77_app:app --host 0.0.0.0 --port 8000`

## Data hierarchy
1. Upstox: live market feed through preserved authenticated provider layer.
2. NSE: official EOD/provisional institutional reports.
3. CDSL: fortnightly/structural FPI context.
4. Sensibull, StockEdge, Research360, Quantsapp, Trendlyne, EQSIS: reference/cross-check links only; not silently scraped as truth.

## New V77 endpoints
- `/api/v77/health`
- `/api/v77/marketking/{symbol}`
- `/api/v77/institutional`

## Truth policy
No fabricated live quotes, OI, DOM, footprint, participant identity or order-flow. EOD/fortnightly data is never labelled live. Broker execution remains disabled.
