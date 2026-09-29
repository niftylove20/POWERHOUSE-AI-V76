from demo_data import demo_snapshot
from v62_engine import build_v62, record_cross_market, cross_market_intel

m=demo_snapshot()
v=build_v62(m)
assert v['version']=='62.0'
assert v['read_only'] is True
assert 'cross_market' in v['modules']
assert 'volume_profile' in v['modules']
assert 'anchored_vwap' in v['modules']
assert 'depth_persistence' in v['modules']
assert 'breadth_rotation' in v['modules']
# Dead feeds are no longer rendered. Verified GIFT can still be cached/used.
assert all(x.get('market')!='DOW FUTURES' for x in v['modules']['cross_market']['markets'])
record_cross_market('GIFT NIFTY',25250,0.24,'test_fixture',True)
cm=cross_market_intel(m)
assert any(x.get('market')=='GIFT NIFTY' and x.get('price')==25250 for x in cm['markets'])
assert all(x.get('market')!='DOW FUTURES' for x in cm['markets'])
print('V62 TEST PASS — working-feed-only external cue policy')
