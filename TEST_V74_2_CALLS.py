import os, tempfile
os.environ['POWERHOUSE_V74_DB_PATH'] = os.path.join(tempfile.gettempdir(),'powerhouse_v742_test.sqlite3')
try: os.unlink(os.environ['POWERHOUSE_V74_DB_PATH'])
except FileNotFoundError: pass
from v74_engine import WORKSPACE_ARCHITECTURE, call_engine_plan, track_call_plan, emit_call_alert, alert_snapshot, call_journal, build_v74, hot_lane_candidates

def row():
    return {
        'symbol':'TEST','ltp':1000.0,'change_pct':1.8,'volume':500000,'rvol':2.5,
        'futures_oi_change_pct':6.0,'oi_velocity':4.0,'sector_strength':82,'sector_ignition':True,
        'total_buy_qty':900000,'total_sell_qty':250000,'bid':999.6,'ask':1000.4,
        'pattern':'BREAKOUT','pattern_quality':86,'breakout':True,'premium_response':82,'iv':18,'gamma':76,
        'v72_side':'CE','pre_move_stage':'TRIGGER READY','quote_age_sec':1,
    }

def pack():
    return {'hero_state':'TRIGGER READY','expiry':'2026-09-24','multi_strike_confirmation':True,'winner':{
        'side':'CE','strike':1000,'expiry':'2026-09-24','premium':100.0,'liquidity':88,'spread_pct':0.45,'score':90,
        'scores':{'liquidity':88,'theta_risk':25,'oi_flow':82,'premium_response':84,'gamma':78}
    }}

assert len(WORKSPACE_ARCHITECTURE)==9
p=call_engine_plan('TEST',row(),pack())
assert p['action']=='BUY CE', p
assert p['status']=='READY', p
assert p['entry_zone']['ideal'] is not None and p['sl'] is not None and p['targets']['t1'] is not None
assert p['risk_reward']['t1'] is not None
assert p['quality_is_probability'] is False
tracked=track_call_plan(p)
assert tracked.get('model_call_id')
a=emit_call_alert(tracked)
assert a and a['kind']=='CALL_ENGINE' and a['priority'] in ('P0','P1')
assert any(x.get('kind')=='CALL_ENGINE' for x in alert_snapshot(0,50)['items'])
j=call_journal(20)
assert j['rows'] and j['rows'][0]['symbol']=='TEST'
out=build_v74({'fno_universe':[row()],'stocks':[row()],'websocket_connected':True},record=False)
assert out['version']=='74.0'
assert len(out['ui_workspaces'])==9
assert 'calls' in out['workspaces'] and 'flow-technical' in out['workspaces'] and 'journal-audit' in out['workspaces']
assert out.get('shadow_comparison') is not None
assert isinstance(hot_lane_candidates((out.get('radar') or {}).get('candidates') or []), list)
late=row(); late['late_entry']=True
p2=call_engine_plan('TEST',late,pack())
assert p2['action']=='WAIT' and p2['status'] in ('WAIT','DO NOT CHASE','ARMING')
print('TEST_V74_2_CALLS PASS')
