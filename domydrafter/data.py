import csv
import yaml

from pick import Pick, Pool, BoosterBox

dir_root = './'

def generate_nations():
    with open(dir_root + 'gamedata/nations.csv', newline='') as file:
        nations_csv = list(csv.DictReader(file, delimiter='\t'))
    nation_dicts = [{'id': 'n' + nat['id'],
                     'name': nat['name'],
                     'attr' : {'era' : nat['era']}
                    } for nat in nations_csv]
    nation_picks = [Pick(**nat) for nat in nation_dicts]
    with open(dir_root + 'data/nations.yaml', 'w') as output:
        output.write(yaml.dump(nation_picks))

if __name__ == "__main__":
    generate_nations()