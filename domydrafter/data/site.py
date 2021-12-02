from .config import data_dir
from .utils import read_csv, Pick

from typing import Dict, List
from functools import reduce

sites_csv_file = 'MagicSites.csv'

Site = Pick


def generate_sites() -> List[Site]:
    sites_data = read_csv(data_dir + sites_csv_file)
    return list(map(site_pipeline, sites_data))


def site_pipeline(site_data: Dict) -> Site:
    pipeline = [
        s_id,
        s_name,
        s_hrec,
        s_income,
        s_scales,
    ]
    return reduce(lambda n,f: f(n, site_data), pipeline, Site('', '', {}, []))


def s_id(site: Site, site_data: Dict) -> Site:
    return site._replace(id='s' + site_data['id'])


def s_name(site: Site, site_data: Dict) -> Site:
    return site._replace(name=site_data['name'])


def s_hrec(site: Site, site_data: Dict) -> Site:
    hcoms = ['u' + site_data[key] for key in hcom_keys if site_data[key]]
    hmons = ['u' + site_data[key] for key in hmon_keys if site_data[key]]
    if len(hcoms) > 0:
        site.attr['hcom'] = hcoms
    if len(hmons) > 0:
        site.attr['hmon'] = hmons
    return site


hcom_keys = ['hcom' + str(n) for n in range(1,6)]

hmon_keys = ['hmon' + str(n) for n in range(1,6)]


def s_income(site: Site, site_data: Dict) -> Site:
    income = {k:site_data[k] for k in income_keys if site_data[k]}
    if len(income) > 0:
        site.attr['income'] = income
    return site


income_keys = ['F', 'A', 'W', 'E', 'S', 'D', 'N', 'B', 'gold', 'res', 'sup']


def s_scales(site: Site, site_data: Dict) -> Site:
    scales = [site_data[k] for k in scales_keys if site_data[k]]
    if len(scales) > 0:
        site.attr['scales'] = scales
    return site


scales_keys = ['scale1', 'scale2']