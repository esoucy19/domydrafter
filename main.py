import os
import sys
import yaml

from yaml import Loader

import domydrafter.pick
from domydrafter.pick import Pick, Pool, BoosterBox

def init():
    data_files = os.listdir('./data')
    for file in data_files:
        if file.lower().endswith('yaml'):
            with open('./data/' + file, 'r') as f:
                data = list(yaml.load_all(f, Loader))

    user_data_files = os.listdir('./user_data')
    for file in user_data_files:
        if file.lower().endswith('yaml'):
            with open('./user_data/' + file, 'r') as f:
                user_data = list(yaml.load_all(f, Loader))

if __name__ == "__main__":
    init()
    print(Pick.picks)
    if len(sys.argv) != 1:
        box = sys.argv[1]
        num_boosters = int(sys.argv[2])
    for i in range(num_boosters):
        booster = domydrafter.pick.BoosterBox.boxes[box].new_booster()
        for pick in booster:
            print('{}, {}'.format(pick.id, pick.name))