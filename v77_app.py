from __future__ import annotations
from pathlib import Path
import time
from fastapi import HTTPException, Request
from fastapi.responses import FileResponse
import v763_app as legacy
from v77_marketking import institutional_snapshot,auto_trender,why_now

app=legacy.app; app.title='POWERHOUSE AI V77 — MARKET KING'; app.version='77.0'
ROOT=Path(__file__).parent; UI=ROOT/'static'/'v77.html'
app.router.routes[:]=[r for r in app.router.routes if not (getattr(r,'path',None)=='/' and 'GET' in (getattr(r,'methods',None) or set()))]
@app.get('/')
def home():
    if UI.exists():return FileResponse(UI)
    raise HTTPException(503,'V77 UI missing')
@app.get('/api/v77/health')
def health(request:Request):
    x=legacy.health(request)
    return {**x,'version':'77.0','app':'POWERHOUSE AI V77 MARKET KING','modules':36,'architecture':'single-source-of-truth / truth-gated / read-only intelligence'}
@app.get('/api/v77/institutional')
def institutional():return institutional_snapshot()
@app.get('/api/v77/marketking/{symbol}')
def marketking(symbol:str,request:Request,interval:int=5,limit:int=180):
    base=legacy.workstation(symbol,request,interval,limit); trend=auto_trender(base.get('candles'))
    return {'version':'77.0','symbol':base.get('symbol'),'spot':base.get('spot'),'auto_trender':trend,'why_now':why_now(base,trend),'workstation':base,'generated_epoch':time.time(),'execution_enabled':False}
def _promote():
    paths={'/','/api/v77/health','/api/v77/institutional','/api/v77/marketking/{symbol}'}; routes=app.router.routes
    p=[r for r in routes if getattr(r,'path',None) in paths]; rem=[r for r in routes if r not in p]
    i=next((i for i,r in enumerate(rem) if r.__class__.__name__=='Mount'),len(rem)); app.router.routes[:]=rem[:i]+p+rem[i:]
_promote()
