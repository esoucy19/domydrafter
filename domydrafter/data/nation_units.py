from .config import data_dir
from .utils import read_csv

from .nation import Nation
from .site import Site
from .unit import Unit

from typing import Any, Dict, List, Tuple
from functools import reduce

fort_leaders_csv = 'fort_leader_types_by_nation.csv'
nonfort_leaders_csv = 'fort_leader_types_by_nation.csv'
coast_leaders_csv = 'coast_leader_types_by_nation.csv'

fort_troops_csv = 'fort_troop_types_by_nation.csv'
nonfort_troops_csv = 'nonfort_troop_types_by_nation.csv'
coast_troops_csv = 'coast_troop_types_by_nation.csv'

unit_cats = {
    'fl': 'fort_leaders',
    'nl': 'nonfort_leaders',
    'cl': 'coastal_leaders',
    'ft': 'fort_troops',
    'nt': 'nonfort_troops',
    'ct': 'coastal_troops'
}

def nation_units(nations: List[Nation], units: List[Unit], sites: List[Site]):
    fl_data = read_csv(data_dir + fort_leaders_csv)
    nl_data = read_csv(data_dir + nonfort_leaders_csv)
    cl_data = read_csv(data_dir + coast_leaders_csv)

    ft_data = read_csv(data_dir + fort_troops_csv)
    nt_data = read_csv(data_dir + nonfort_troops_csv)
    ct_data = read_csv(data_dir + coast_troops_csv)

    nu_data = {
        'fl': fl_data,
        'nl': nl_data,
        'cl': cl_data,
        'ft': ft_data,
        'nt': nt_data,
        'ct': ct_data,
    }
    return (list(map(lambda n: nat_unit_pipeline(n, units, nu_data, sites), nations)),
            units)


def nat_unit_pipeline(nation: Nation, units: List[Unit], nu_data: Dict[str, List[Dict]], sites: List[Site]) -> Nation:
    pipeline = [
        nu_units,
        nu_cap_units
    ]

    def nat_filter(cat_units):
        cat, units = cat_units
        res = (cat, list(filter(nat_units, units)))
        return res

    def nat_units(unit):
        return 'n' + str(unit['nation_number'])  == nation.id

    nat_data = dict(map(nat_filter, nu_data.items()))
    return reduce(lambda n, f: f(n, units, nat_data, sites), pipeline, nation)


def nu_units(nation: Nation, units: List[Unit], nat_data: Dict[str, List[Dict]], sites: List[Site]) -> Nation:
    list(map(lambda cat_key, cat_name: cat_to_nation(nation, nat_data[cat_key], cat_name, units),
        unit_cats.keys(), unit_cats.values()))
    return nation


def cat_to_nation(nation: Nation, cat: List[Dict], cat_name: str, units: List[Unit]) -> Nation:
    unit_ids = list(map(lambda data: 'u' + str(data['monster_number']), cat))
    nat_units = list(filter(lambda unit: unit.id in unit_ids, units))
    def nat_to_unit(unit):
        if 'nations' not in unit.attr:
            unit.attr['nations'] = []
        unit.attr['nations'].append(nation.id)
        if 'units' not in nation.attr:
            nation.attr['units'] = dict()
        if cat_name not in nation.attr['units']:
            nation.attr['units'][cat_name] = []
        nation.attr['units'][cat_name].append(unit.id)
    list(map(nat_to_unit, nat_units))


def nu_cap_units(nation: Nation, units: List[Unit], nat_data: Dict[str, List[Dict]], sites: List[Site]) -> Nation:
    nat_sites = list(filter(lambda site: site.id in nation.attr['cap_sites'], sites))
    def nat_units(site):
        if 'hcom' in site.attr:
            if 'cap_leaders' not in nation.attr['units']:
                nation.attr['units']['cap_leaders'] = []
            nation.attr['units']['cap_leaders'] += site.attr['hcom']
        if 'hmon' in site.attr:
            if 'cap_troops' not in nation.attr['units']:
                nation.attr['units']['cap_troops'] = []
            nation.attr['units']['cap_troops'] += site.attr['hmon']
    list(map(nat_units, nat_sites))
    return nation