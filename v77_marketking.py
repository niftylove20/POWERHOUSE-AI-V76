from __future__ import annotations
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any
import math, re, time, httpx

NSE_FII_DII='https://www.nseindia.com/reports/fii-dii'
CDSL_FPI='https://www.cdslindia.com/publications/FII/FortnightlySecWisePages/September%2015,%202026.html'
REFERENCES={
 'Sensibull':'https://web.sensibull.com/fii-dii-data','StockEdge':'https://web.stockedge.com/fii-activity',
 'Research360':'https://www.research360.in/market/fii-dii-data','Quantsapp':'https://web.quantsapp.com/participant-data/fii-dii-data',
 'Trendlyne':'https://trendlyne.com/futures-options/reports/participants-wise-oi/','EQSIS':'https://www.eqsis.com/primer/fii-open-interest-analysis.php'}

def num(x):
    try:
        v=float(str(x).replace(',','').replace('₹','').replace('%','').strip()); return v if math.isfinite(v) else None
    except:return None

class TableParser(HTMLParser):
    def __init__(self): super().__init__(); self.tables=[]; self.t=None; self.r=None; self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=='table': self.t=[]
        elif tag=='tr' and self.t is not None:self.r=[]
        elif tag in ('td','th') and self.r is not None:self.cell=[]
    def handle_data(self,d):
        if self.cell is not None:self.cell.append(d)
    def handle_endtag(self,tag):
        if tag in ('td','th') and self.cell is not None:
            self.r.append(re.sub(r'\s+',' ',' '.join(self.cell)).strip()); self.cell=None
        elif tag=='tr' and self.r is not None:
            if any(self.r):self.t.append(self.r)
            self.r=None
        elif tag=='table' and self.t is not None:
            if self.t:self.tables.append(self.t)
            self.t=None

def fetch_tables(url:str)->dict:
    headers={'User-Agent':'Mozilla/5.0 (compatible; POWERHOUSE-AI/77; +read-only-market-intelligence)','Accept':'text/html,application/xhtml+xml'}
    try:
        with httpx.Client(timeout=12,follow_redirects=True,headers=headers) as c:r=c.get(url)
        r.raise_for_status(); p=TableParser(); p.feed(r.text)
        return {'ok':True,'url':url,'status':r.status_code,'tables':p.tables,'fetched_epoch':time.time()}
    except Exception as e:return {'ok':False,'url':url,'error':type(e).__name__+': '+str(e)[:180],'tables':[],'fetched_epoch':time.time()}

def institutional_snapshot()->dict:
    nse=fetch_tables(NSE_FII_DII); cdsl=fetch_tables(CDSL_FPI)
    return {'source_policy':'NSE official = primary/provisional cash activity; CDSL = structural/final FPI context where published; third-party pages are references/cross-checks only.',
      'nse':{'role':'OFFICIAL_EOD','data':nse},'cdsl':{'role':'FORTNIGHTLY_STRUCTURAL','data':cdsl},
      'references':REFERENCES,'quality':'VERIFIED_SOURCES_AVAILABLE' if nse['ok'] or cdsl['ok'] else 'SOURCE_UNAVAILABLE',
      'warning':'Never relabel EOD/fortnightly data as live. No values are synthesized when a source is unavailable.'}

def candle_rows(candles):
    out=[]
    for c in candles or []:
        if isinstance(c,dict): o,h,l,cl,v=[num(c.get(k) or c.get(k[0])) for k in ('open','high','low','close','volume')]
        elif isinstance(c,(list,tuple)) and len(c)>=6:o,h,l,cl,v=map(num,(c[1],c[2],c[3],c[4],c[5]))
        else:continue
        if None not in (o,h,l,cl):out.append((o,h,l,cl,v or 0))
    return out

def auto_trender(candles)->dict:
    r=candle_rows(candles)
    if len(r)<20:return {'available':False,'state':'INSUFFICIENT_DATA','confidence':'LOW'}
    closes=[x[3] for x in r]; vols=[x[4] for x in r]
    ema=lambda n: sum(closes[-n:])/n
    e5,e20=ema(5),ema(20); slope=(e5-(sum(closes[-10:-5])/5))/max(abs(e5),1)*100
    recent=r[-8:]; hh=recent[-1][1]>=max(x[1] for x in recent[:-1]); ll=recent[-1][2]<=min(x[2] for x in recent[:-1])
    score=(1 if e5>e20 else -1)+(1 if slope>.03 else -1 if slope<-.03 else 0)+(1 if hh else -1 if ll else 0)
    state={3:'STRONG_UPTREND',2:'UPTREND',1:'WEAK_UPTREND',0:'RANGE',-1:'WEAK_DOWNTREND',-2:'DOWNTREND',-3:'STRONG_DOWNTREND'}[score]
    rv=(sum(vols[-5:])/5)/(sum(vols[-20:])/20) if sum(vols[-20:]) else None
    return {'available':True,'state':state,'score':score,'ma5':round(e5,2),'ma20':round(e20,2),'ma5_slope_pct':round(slope,3),'relative_volume_5v20':round(rv,2) if rv else None,'evidence':['MA5 above MA20' if e5>e20 else 'MA5 below MA20',f'MA5 slope {slope:.3f}%','recent higher-high' if hh else 'recent lower-low' if ll else 'no fresh structural extreme'],'confidence':'HIGH' if abs(score)>=2 else 'MEDIUM' if score else 'LOW','policy':'Descriptive trend classification, not a guaranteed trade signal'}

def why_now(base:dict,trend:dict)->dict:
    d=base.get('derivatives') or {}; available=bool(d)
    ev=[]
    if trend.get('available'):ev.append('Auto Trender: '+trend['state'])
    if available:ev.append('Derivatives payload available for cross-check')
    else:ev.append('Derivatives confirmation unavailable')
    return {'what_changed':trend.get('state','INSUFFICIENT_DATA'),'supporting_evidence':ev,'contradicting_evidence':[], 'confirmation_needed':'Price structure + breadth + reliable derivatives/order-flow agreement','invalidation':'Trend structure reverses with confirming breadth/volume','data_freshness':'Use provider_status timestamps','no_edge':not trend.get('available')}
