# POWERHOUSE AI V74 — deploy overlay

## Verified base
- Repository: `ravumeet1320-bot/Powerhouse-ai-v71`
- Verified main base SHA before V74 work: `8d4963b8396366cda8256680cc9053f1fc491658`
- Git history contains V72.2 then V73 LTS; no V72.3 branch/commit was found.
- V74 therefore preserves V72.2 through the current V73 LTS cumulative stack and adds a new orchestration/router/UI layer.

## Overlay files
Copy these onto the repo root:
- `v74_engine.py`
- `v74_app.py`
- `V74_LOCKED_ARCHITECTURE.txt`
- `CHANGELOG_v74.txt`
- `TEST_V74.py`
- `static/v74.html`

Replace only the start command in `render.yaml` and `Dockerfile` so Uvicorn starts `v74_app:app`. The V74 wrapper mounts the legacy `app:app` under `/`, so all existing cumulative `/api/vXX`, OAuth, static and health routes stay reachable while V74 owns `/` and `/api/v74/*`.

## Required pre-deploy checks
```bash
python -m compileall -q .
python TEST_V74.py
python TEST_V73_LTS.py
python TEST_V72_2.py
python - <<'PY'
from pathlib import Path
s=Path('static/v74.html').read_text()
Path('/tmp/v74-ui.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0])
PY
node --check /tmp/v74-ui.js
```
Then run the full regression suite already used for V73 LTS.

## V74 endpoints
- `GET /api/v74/status`
- `GET /api/v74/tabs`
- `GET /api/v74/coverage`
- `GET /api/v74/radar`
- `GET /api/v74/big-move`
- `GET /api/v74/hero/{symbol}`
- `GET /api/v74/chart/{symbol}`
- `GET /api/v74/option-chain/{symbol}`
- `GET /api/v74/missed-moves`
- `GET /api/v74/performance`
- `GET /api/v74/forensics`
- `GET /api/v74/replay/{symbol}`
- `POST /api/v74/telemetry/ui`

## Production truth locks
- No V74 mock/demo market values are substituted when live authentication is unavailable.
- Missing scouts are `UNAVAILABLE`, not fake neutral scores.
- No broker order placement or automatic execution.
- No guaranteed profit/win-rate claim.
- Every observed meaningful move is expected to be accounted for by detection or explicit miss classification.

## Rollback
Restore the prior Render/Docker start command to `uvicorn app:app ...` or redeploy the recorded pre-V74 SHA.
