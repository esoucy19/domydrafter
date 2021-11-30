import pytest
import yaml

from yaml import Loader, SafeLoader, UnsafeLoader

from domydrafter.pick import Pick, Pool, BoosterBox

sample_picks_data = [
    (1, 'militia'),
    (2, 'commander'),
    (3, 'archer'),
    (4, 'heavy cavalry')
]

#sample_picks = { (d[1]):Pick(*d) for d in sample_picks_data}

#common = Pool('common', [sample_picks['militia'], sample_picks['archer']])
#uncommon = Pool('uncommon', [sample_picks['commander']])
#rare = Pool('rare', [sample_picks['heavy cavalry']])

#booster_format = [ (common, 2), (uncommon, 1), (rare, 1) ]

#box = BoosterBox('box1', booster_format)
#print(*box.new_booster())

obj = yaml.load(
"""
--- !Pick
id: u1001
name: militia
attr:
tags:
""", Loader)

obj2 = yaml.load(
"""
--- !Pick
id: u1002
name: heavy infantry
attr:
tags:
""", Loader)

obj3 = yaml.load(
"""
--- !Pick
id: u1001
name: militia modified
attr:
tags:
""", Loader)

obj4 = yaml.load(
"""
--- !Pool
name: pool1
picks:
- u1001
- u1002] }
""", Loader)
print(obj4)
print(Pick.picks)
print(Pool.pools)
raise()
