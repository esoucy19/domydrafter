from .config import data_dir
from .utils import read_csv

from .nation import Nation
from .site import Site

from typing import Dict, List, Tuple
from functools import reduce

nations_attr_csv_file = 'attributes_by_nation.csv'


def nation_sites(nations: List[Nation], sites: List[Site]) -> Tuple[List[Nation], List[Site]]:
    nations_attr = read_csv(data_dir + nations_attr_csv_file)
    return (list(map(lambda n: nat_site_pipeline(n, sites, nations_attr), nations)), sites)


def nat_site_pipeline(nation: Nation, sites: List[Site], nations_attr: List[Dict]) -> Nation:
    pipeline = [
        nat_site,
    ]
    nation_attr = list(filter(lambda na: 'n' + na['nation_number'] == nation.id, nations_attr))


    return reduce(lambda n, f: f(n, sites, nation_attr), pipeline, nation)


def nat_site(nation: Nation, sites: List[Site], nation_attr: List[Dict]) -> Nation:
    nation_sites = list(map(
        lambda s: 's' + str(s['raw_value']),
        filter(
            lambda s: s['attribute'] == '52',
            nation_attr)
    ))
    nation.attr['cap_sites'] = nation_sites

    sites_nation = list(filter(lambda s: s.id in nation_sites, sites))
    for site in sites_nation:
        site.attr['nation'] = nation.id
    return nation
