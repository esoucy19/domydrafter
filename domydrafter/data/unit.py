from .config import data_dir
from .utils import read_csv, magic_paths, magic_path_keys

from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple

units_csv_file = 'BaseU.csv'

@dataclass
class Unit:
    id: str
    name: str
    attr: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


def generate_units() -> List[Unit]:
    units: List[Unit]
    units = []

    units_csv: List[Dict]
    units_csv = read_csv(data_dir + units_csv_file)

    for unit_csv in units_csv:
        id = unit_csv['id']
        name = unit_csv['name']
        attr = generate_attr(unit_csv)

    return units


def generate_attr(unit_csv: Dict) -> Dict[str, Any]:
    attr = dict()
    attr = get_paths(attr, unit_csv)

    return attr


def get_path_data(unit_csv: Dict) -> Dict:
    path_data = dict()
    for key in magic_path_keys:
        if (unit_csv[key]):
            path_data[key] = unit_csv[key]
    return path_data


def decode_paths_mask(mask: int) -> List[str]:
    decoded_paths = []
    bits = "{:016b}".format(mask)
    for i, path in enumerate(reversed(magic_paths)):
        if bits[i] == '1':
            decoded_paths.append(path)
    return list(reversed(decoded_paths))


def process_paths_data(unit_csv: Dict) -> Dict:
    processed_paths = dict()
    for key in unit_csv:
        key: str
        if key.startswith('rand'):
            n = key[-1]
            rand = unit_csv[key]
            nbr = unit_csv['nbr' + n]
            mask = unit_csv['mask' + n]
            rand_paths: List[str]
            rand_paths = decode_paths_mask(mask)
            if 'random' not in processed_paths:
                processed_paths['random'] = []
            processed_paths['random'].append((rand, rand_paths, nbr))
        elif key in magic_paths:
            processed_paths[key] = unit_csv[key]
    return processed_paths


def get_paths(attr_dict: Dict, unit_csv: Dict) -> Dict:
    paths = process_paths_data(unit_csv)
    if len(paths) > 0:
        attr_dict['paths'] = paths
    return attr_dict


def generate_tags(unit_csv: Dict) -> List[str]:
    tags: List[str]
    tags = []


# Utility functions
