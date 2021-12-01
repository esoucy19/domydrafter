from .config import data_dir
from .utils import eras_dict, read_csv, Pick

from typing import Dict, List
from functools import reduce

nations_csv_file = 'nations.csv'

Nation = Pick

def generate_nations() -> List[Nation]:
    nations_data = read_csv(data_dir + nations_csv_file)
    return list(map(nation_pipeline, nations_data))


def nation_pipeline(nation_data: Dict) -> Nation:
    pipeline = [
        n_id,
        n_name,
        n_era
    ]
    return reduce(lambda n,f: f(n, nation_data), pipeline, Nation('', '', {}, []))


def n_id(nation: Nation, nation_data: Dict) -> Nation:
    return nation._replace(id='n' + nation_data['id'])


def n_name(nation: Nation, nation_data: Dict) -> Nation:
    return nation._replace(name=nation_data['file_name_base'])


def n_era(nation: Nation, nation_data: Dict) -> Nation:
    nation.attr['era'] = eras_dict[nation_data['era']]
    return nation