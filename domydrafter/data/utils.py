import csv
from collections import namedtuple
from typing import List
from typing import List

Pick = namedtuple('Pick', ['id', 'name', 'attr', 'tags'], defaults=['', '', None, None])
magic_paths = ['F', 'A', 'W', 'E', 'S', 'D', 'N', 'B', 'H']
magic_path_keys: List
eras_dict = {'1': 'ea', '2': 'ma', '3': 'la'}


def read_csv(path):
    with open(path, newline='') as file:
        data = list(csv.DictReader(file, delimiter='\t'))
    return data


def generate_path_keys() -> List[str]:
    rand_keys = ['rand', 'nbr', 'mask']
    path_keys = [] + magic_paths
    for i in range(1,5):
        path_keys += [key + str(i) for key in rand_keys]
    return path_keys

magic_path_keys = generate_path_keys()