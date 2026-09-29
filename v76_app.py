from __future__ import annotations
"""POWERHOUSE AI V76.2 mobile-first Order Flow workstation shell.
Additive UI release over the locked V74.3 backend. No broker execution is enabled.
"""
from pathlib import Path
from fastapi import HTTPException, Request
from fastapi.responses import FileResponse
import v743_app as legacy

app = legacy.app
app.title = "POWERHOUSE AI V76.2 — Order Flow Ultra"
app.version = "76.2"
ROOT = Path(__file__).parent
UI = ROOT / "static" / "v762.html"

# Own the root only; all legacy API routes remain intact.
app.router.routes[:] = [r for r in app.router.routes if not (getattr(r, "path", None) == "/" and "GET" in (getattr(r, "methods", None) or set()))]

@app.get("/")
def home():
    if UI.exists():
        return FileResponse(UI)
    raise HTTPException(status_code=503, detail="V76.2 UI asset missing")

@app.get("/api/v76/health")
def v76_health(request: Request):
    svc = legacy.base.request_service(request)
    try:
        s = svc.status() or {}
    except Exception:
        s = {}
    return {
        "ok": True,
        "app": "POWERHOUSE AI V76.2",
        "version": "76.2",
        "mode": "READ_ONLY_INTELLIGENCE",
        "orders_enabled": False,
        "execution_enabled": False,
        "upstox_authenticated": bool(getattr(svc, "authenticated", False)),
        "data_status": s.get("data_status") or "UNAVAILABLE",
        "truth_policy": "Never fabricate unavailable live order-flow/OI/DOM data",
        "legacy": "/legacy" if any(getattr(r,'path',None)=='/legacy' for r in app.router.routes) else "V74.3 APIs preserved",
    }

# FastAPI/Starlette resolves routes in declaration order. The preserved legacy
# application includes a catch-all Mount, so keep V76.2 routes ahead of it.
def _promote_v76_routes() -> None:
    routes = app.router.routes
    promoted = [r for r in routes if getattr(r, "path", None) in {"/", "/api/v76/health"}]
    if not promoted:
        return
    remaining = [r for r in routes if r not in promoted]
    mount_at = next((i for i, r in enumerate(remaining) if r.__class__.__name__ == "Mount"), len(remaining))
    app.router.routes[:] = remaining[:mount_at] + promoted + remaining[mount_at:]

_promote_v76_routes()
