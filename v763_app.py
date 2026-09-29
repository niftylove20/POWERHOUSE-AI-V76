from __future__ import annotations
from pathlib import Path
import time
from fastapi import HTTPException, Request
from fastapi.responses import FileResponse
import v743_app as legacy
from v763_engine import profile_from_candles,reconstructed_flow,participation

app=legacy.app
app.title='POWERHOUSE AI V76.3 — LIVE-WIRED ORDER FLOW'
app.version='76.3'
ROOT=Path(__file__).parent; UI=ROOT/'static'/'v763.html'
app.router.routes[:]=[r for r in app.router.routes if not (getattr(r,'path',None)=='/' and 'GET' in (getattr(r,'methods',None) or set()))]

@app.get('/')
def home():
    if UI.exists(): return FileResponse(UI)
    raise HTTPException(503,'V76.3 UI missing')

@app.get('/api/v76/health')
def health(request:Request):
    svc=legacy.base.request_service(request)
    try:s=svc.status() or {}
    except Exception:s={}
    state=s.get('data_status') or 'UNAVAILABLE'; market=bool(s.get('market_session_open'))
    label='LIVE' if state=='LIVE' and market else ('MARKET CLOSED' if not market and state in {'LIVE','REST','STALE'} else state)
    return {'ok':True,'version':'76.3','app':'POWERHOUSE AI V76.3','mode':'READ_ONLY_INTELLIGENCE','orders_enabled':False,'execution_enabled':False,'upstox_authenticated':bool(getattr(svc,'authenticated',False)),'data_status':state,'display_status':label,'market_session_open':market,'tick_age_sec':s.get('tick_age_sec'),'rest_age_sec':s.get('rest_age_sec'),'truth_policy':'No fabricated market/OI/DOM/footprint data'}

@app.get('/api/v76/workstation/{symbol}')
def workstation(symbol:str,request:Request,interval:int=5,limit:int=180):
    base=legacy.v743_intelligence(symbol,request,interval,limit)
    candles=base.get('candles') or []; deriv=base.get('derivatives') or {}
    prof=profile_from_candles(candles); flow=reconstructed_flow(candles); part=participation(base.get('spot'),deriv)
    svc=legacy.base.request_service(request)
    try:status=svc.status() or {}
    except Exception:status={}
    # True executed bid×ask classification is deliberately unavailable unless a future feed supplies it.
    true_flow={'available':False,'classification':'INSUFFICIENT','reason':'Current provider payload does not prove exchange aggressor-side executed volume by price. Reconstructed proxy is shown separately.'}
    return {'version':'76.3','symbol':base.get('symbol'),'spot':base.get('spot'),'candles':candles,'levels':base.get('levels'),'derivatives':deriv,'level_attack':base.get('level_attack'),'candidate':base.get('candidate'),'profile':prof,'reconstructed_flow':flow,'true_flow':true_flow,'participation':part,'provenance':base.get('provenance'),'provider_status':status,'errors':base.get('errors') or [],'read_only':True,'execution_enabled':False,'generated_epoch':time.time()}

def _promote():
    paths={'/','/api/v76/health','/api/v76/workstation/{symbol}'}; routes=app.router.routes
    p=[r for r in routes if getattr(r,'path',None) in paths]; rem=[r for r in routes if r not in p]
    i=next((i for i,r in enumerate(rem) if r.__class__.__name__=='Mount'),len(rem)); app.router.routes[:]=rem[:i]+p+rem[i:]
_promote()
