from .config import data_dir
from .utils import read_csv, magic_paths, magic_path_keys, Pick

from typing import Dict, List
from functools import reduce

units_csv_file = 'BaseU.csv'

Unit = Pick

def generate_units() -> List[Unit]:
    units_data = read_csv(data_dir + units_csv_file)
    return list(map(unit_pipeline, units_data))


def unit_pipeline(unit_data: Dict) -> Unit:
    pipeline = [
        u_id,
        u_name,
        u_paths,
        u_sacred,
        u_mage,
        u_priest
    ]
    return reduce(lambda u,f: f(u, unit_data), pipeline, Unit('', '', {}, []))


def u_id(unit: Unit, unit_data: Dict) -> Unit:
    return unit._replace(id='u' + unit_data['id'])


def u_name(unit: Unit, unit_data: Dict) -> Unit:
    return unit._replace(name=unit_data['name'])


def u_paths(unit: Unit, unit_data: Dict) -> Unit:
    paths = get_paths(unit_data)
    if len(paths) != 0:
        unit.attr['paths'] = paths
    return unit


def u_sacred(unit: Unit, unit_data: Dict) -> Unit:
    if unit_data['holy'] and 'sacred' not in unit.tags:
        unit.tags.append('sacred')
    return unit


def u_mage(unit: Unit, unit_data: Dict) -> Unit:
    if 'paths' in unit.attr:
        if len(unit.attr['paths']) == 1 and 'H' in unit.attr['paths']:
            pass
        else:
            if 'mage' not in unit.tags:
                unit.tags.append('mage')
    return unit


def u_priest(unit: Unit, unit_data: Dict) -> Unit:
    if 'paths' in unit.attr and 'H' in unit.attr['paths'] and 'priest' not in unit.tags:
        unit.tags.append('priest')
    return unit


def get_paths(unit_data: Dict) -> Dict:
    paths_data = get_paths_data(unit_data)
    paths = process_paths_data(paths_data)
    return paths


def get_paths_data(unit_data: Dict) -> Dict:
    path_data = dict()
    for key in magic_path_keys:
        if key in unit_data and unit_data[key]:
            path_data[key] = unit_data[key]
    return path_data


def process_paths_data(unit_paths: Dict) -> Dict:
    paths = dict()
    for key in unit_paths:
        if key.startswith('rand'):
            n = key[-1]
            rand = unit_paths[key]
            nbr = unit_paths['nbr' + n]
            mask = unit_paths['mask' + n]
            rand_paths: List[str]
            rand_paths = decode_paths_mask(mask)
            if 'random' not in paths:
                paths['random'] = []
            paths['random'].append((rand, rand_paths, nbr))
        elif key in magic_paths:
            paths[key] = unit_paths[key]
    return paths


def decode_paths_mask(mask: int) -> List[str]:
    decoded_paths = []
    bits = "{:016b}".format(int(mask))
    for i, path in enumerate(reversed(magic_paths)):
        if bits[i] == '1':
            decoded_paths.append(path)
    return list(reversed(decoded_paths))
