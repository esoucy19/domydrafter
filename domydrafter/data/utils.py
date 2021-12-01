import csv

from typing import List

magic_paths = ['F', 'A', 'W', 'E', 'S', 'D', 'N', 'B', 'H']

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
