from __future__ import annotations
from typing import Any
import math, time

def f(v, default=None):
    try:
        x=float(v); return x if math.isfinite(x) else default
    except Exception:return default

def profile_from_candles(candles:list[Any], bins:int=24)->dict:
    rows=[]
    for c in candles or []:
        if isinstance(c,dict):
            h=f(c.get('high') or c.get('h')); l=f(c.get('low') or c.get('l')); cl=f(c.get('close') or c.get('c')); v=f(c.get('volume') or c.get('v'),0) or 0
        elif isinstance(c,(list,tuple)) and len(c)>=6:
            h,l,cl,v=f(c[2]),f(c[3]),f(c[4]),f(c[5],0) or 0
        else: continue
        if None not in (h,l,cl): rows.append((h,l,cl,max(0,v)))
    if not rows:return {'available':False,'source':'UNAVAILABLE'}
    lo=min(x[1] for x in rows); hi=max(x[0] for x in rows)
    if hi<=lo:return {'available':False,'source':'UNAVAILABLE'}
    step=(hi-lo)/bins; vols=[0.0]*bins
    for h,l,cl,v in rows:
        a=max(0,min(bins-1,int((l-lo)/step))); b=max(0,min(bins-1,int((h-lo)/step)))
        n=max(1,b-a+1)
        for i in range(a,b+1): vols[i]+=v/n
    total=sum(vols); poc=max(range(bins),key=lambda i:vols[i]); chosen={poc}; acc=vols[poc]
    left,right=poc-1,poc+1
    while total and acc/total<0.70 and (left>=0 or right<bins):
        lv=vols[left] if left>=0 else -1; rv=vols[right] if right<bins else -1
        if rv>lv: chosen.add(right); acc+=rv; right+=1
        else: chosen.add(left); acc+=lv; left-=1
    price=lambda i: lo+(i+.5)*step
    return {'available':True,'vah':round(price(max(chosen)),2),'val':round(price(min(chosen)),2),'poc':round(price(poc),2),'histogram':[round(x,2) for x in vols], 'source':'CANDLE_VOLUME_PROFILE_APPROX','value_area_pct':70}

def reconstructed_flow(candles:list[Any])->dict:
    bars=[]; cvd=0.0
    for c in (candles or [])[-40:]:
        if isinstance(c,dict): o,cl,v=f(c.get('open') or c.get('o')),f(c.get('close') or c.get('c')),f(c.get('volume') or c.get('v'),0) or 0
        elif isinstance(c,(list,tuple)) and len(c)>=6:o,cl,v=f(c[1]),f(c[4]),f(c[5],0) or 0
        else:continue
        if None in (o,cl):continue
        delta=v if cl>o else -v if cl<o else 0.0; cvd+=delta; bars.append(round(delta,2))
    if not bars:return {'available':False,'classification':'INSUFFICIENT','bars':[],'cvd':None}
    pos=sum(x for x in bars if x>0); neg=abs(sum(x for x in bars if x<0)); den=pos+neg
    buy=round(pos/den*100,1) if den else None
    return {'available':True,'classification':'RECONSTRUCTED','method':'Candle-direction volume proxy; NOT executed Bid×Ask flow','bars':bars,'cvd':round(cvd,2),'buy_aggression_proxy':buy,'sell_aggression_proxy':round(100-buy,1) if buy is not None else None}

def participation(spot, chain_analytics:dict)->dict:
    atm=(chain_analytics or {}).get('atm') or {}; ce=(atm.get('ce') or {}); pe=(atm.get('pe') or {})
    ce_d=f(ce.get('oi_change')); pe_d=f(pe.get('oi_change'))
    if ce_d is None and pe_d is None:return {'available':False,'state':'INSUFFICIENT_DATA'}
    # Evidence labels only; not institutional identity.
    vals={'fresh_long':0,'fresh_short':0,'short_covering':0,'long_unwinding':0}
    if pe_d is not None and pe_d>0: vals['fresh_long']+=50
    if ce_d is not None and ce_d<0: vals['short_covering']+=50
    if ce_d is not None and ce_d>0: vals['fresh_short']+=50
    if pe_d is not None and pe_d<0: vals['long_unwinding']+=50
    return {'available':True,'scores':vals,'state':max(vals,key=vals.get).upper(),'policy':'Price/OI evidence classifier; not participant identity'}
