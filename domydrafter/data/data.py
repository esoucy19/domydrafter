import csv
import yaml

from pick import Pick, Pool, BoosterBox

dir_root = '../'
datadir = dir_root + 'gamedata/'

def read_csv(filename):
    with open(dir_root + filename, newline='') as file:
        data = list(csv.DictReader(file, delimiter='\t'))
    return data


def generate_nation_attr(nation_data, nation_attr_csv):
    attr = dict()
    nat_id = nation_data['id']

    # Get era
    era_map = {'1': 'ea', '2': 'ma', '3': 'la'}
    attr['era'] = era_map[nation_data['era']]

    # Get sites
    natsites = [
        att['raw_value']
        for att in nation_attr_csv
        if att['nation_number'] == nat_id
            and att['attribute'] == '52'
    ]
    attr['sites'] = natsites
    return attr

def generate_nations():
    nations_csv = read_csv('gamedata/nations.csv')
    nations_attr_csv = read_csv('gamedata/attributes_by_nation.csv')
    nation_dicts = [{'id': 'n' + nat['id'],
                     'name': nat['file_name_base'],
                     'attr': generate_nation_attr(nat, nations_attr_csv)
                    } for nat in nations_csv]
    nation_picks = [Pick(**nat) for nat in nation_dicts]
    era_filter = lambda nat, era: nat.attr['era'] == era
    ea_filter = lambda nat: era_filter(nat, '1')
    ma_filter = lambda nat: era_filter(nat, '2')
    la_filter = lambda nat: era_filter(nat, '3')
    ea_nations = Pool('ea_nations', list(filter(ea_filter, nation_picks)))
    ma_nations = Pool('ma_nations', list(filter(ma_filter, nation_picks)))
    la_nations = Pool('la_nations', list(filter(la_filter, nation_picks)))
    all_nations = Pool('all_nations', picks=[], merge=['ea_nations', 'ma_nations', 'la_nations'])

    with open(dir_root + 'data/0nations.yaml', 'w') as output:
        output.write(yaml.dump_all(
            [nation_picks,
             ea_nations,
             ma_nations,
             la_nations,
             all_nations
             ]
        ))


def generate_unit_tags(unit_data, hrec):
    """
    Generate unit tags from a dict of the unit's csv data and a dict of all
    sites with special unit recruits.
    :param unit_data: The dict of csv data for the unit
    :param hrec: List of sites containing hmon and hcom rectruits
    :return: List of tags to apply to the unit.
    """
    tags = set()
    unit_id = unit_data['id']
    # str
    if unit_data['rt'] == 2:
        tags.add('slow_to_recruit')
    if unit_data['holy'] == 1:
        tags.add('sacred')
    if unit_data['H']:
        tags.add('priest')
    if any([
        unit_data['F'],
        unit_data['A'],
        unit_data['W'],
        unit_data['E'],
        unit_data['S'],
        unit_data['D'],
        unit_data['N'],
        unit_data['B'],
         ]):
        tags.add('mage')
    for site in hrec.values():
        if unit_id in site['hmon'] or unit_id in site['hcom']:
            tags.add('cap_only')
    return tags

def generate_units():
    # Generate all unit picks
    units_csv = read_csv('gamedata/BaseU.csv')
    magicsites_csv = read_csv('gamedata/MagicSites.csv')
    hrec = dict()
    for site_data in magicsites_csv:
        site = dict()
        site['id'] = site_data['id']
        site['hmon'] = set()
        site['hcom'] = set()
        site['hmon'].add(site_data['hmon1'])
        site['hmon'].add(site_data['hmon2'])
        site['hmon'].add(site_data['hmon3'])
        site['hmon'].add(site_data['hmon4'])
        site['hmon'].add(site_data['hmon5'])
        site['hcom'].add(site_data['hcom1'])
        site['hcom'].add(site_data['hcom2'])
        site['hcom'].add(site_data['hcom3'])
        site['hcom'].add(site_data['hcom4'])
        site['hcom'].add(site_data['hcom5'])
        hrec[site['id']] = site

    unit_dicts = [{'id': 'u' + unit['id'],
                   'name': unit['name'],
                   'tags' : generate_unit_tags(unit, hrec)
                  } for unit in units_csv]
    unit_picks = [Pick(**unit) for unit in unit_dicts]

    with open(dir_root + 'data/0units.yaml', 'w') as output:
        output.write(yaml.dump(unit_picks))

    # Generate nation pools
    nations_csv = read_csv('gamedata/nations.csv')
    nations_dict = {nat['id']: nat['file_name_base'] for nat in nations_csv}

    fln_csv = read_csv('gamedata/fort_leader_types_by_nation.csv')
    ftn_csv = read_csv('gamedata/fort_troop_types_by_nation.csv')
    nfln_csv = read_csv('gamedata/nonfort_leader_types_by_nation.csv')
    nftn_csv = read_csv('gamedata/nonfort_troop_types_by_nation.csv')
    cl_csv = read_csv('gamedata/coast_leader_types_by_nation.csv')
    ct_csv = read_csv('gamedata/coast_troop_types_by_nation.csv')


    def id_filter(unit, nat_num):
        return unit['nation_number'] == nat_num

    nation_pools = []
    for nat_id in nations_dict:
        def nat_filter(unit):
            return id_filter(unit, nat_id)
        nat_fort_leaders = filter(nat_filter, fln_csv)
        nat_fort_troops = filter(nat_filter, ftn_csv)
        nat_nonfort_leaders = filter(nat_filter, nfln_csv)
        nat_nonfort_troops = filter(nat_filter, nftn_csv)
        nat_coast_leaders = filter(nat_filter, cl_csv)
        nat_coast_troops = filter(nat_filter, ct_csv)

        nat_cap_only_leaders = []
        nat_cap_only_troops = []
        nation_pick = Pick.picks['n' + nat_id]
        for site_id in nation_pick.attr['sites']:
            site = hrec[site_id]
            for hcom in site['hcom']:
                if hcom:
                    nat_cap_only_leaders.append('u' + hcom)
            for hmon in site['hmon']:
                if hmon:
                    nat_cap_only_troops.append('u' + hmon)

        def unit_pool(utype, pool):
            return Pool(
                    nations_dict[nat_id] + '_' + utype,
                    picks=sorted(['u' + unit['monster_number'] for unit in pool])
                    )
        nat_fort_l_pool = unit_pool('fort_leaders', nat_fort_leaders)
        nat_fort_t_pool = unit_pool('fort_troops', nat_fort_troops)
        nat_nonfort_l_pool = unit_pool('nonfort_leaders', nat_nonfort_leaders)
        nat_nonfort_t_pool = unit_pool('nonfort_troops', nat_nonfort_troops)
        nat_coast_l_pool = unit_pool('coastal_leaders', nat_coast_leaders)
        nat_coast_t_pool = unit_pool('coastal_troops', nat_coast_troops)

        nat_co_l_pool = Pool(nations_dict[nat_id] + '_cap_only_leaders', nat_cap_only_leaders)
        nat_co_t_pool = Pool(nations_dict[nat_id] + '_cap_only_troops', nat_cap_only_troops)

        natname = nations_dict[nat_id]
        nat_leaders = Pool(natname + '_leaders', picks=[], merge=[
            natname + '_fort_leaders',
            natname + '_nonfort_leaders',
            natname + '_cap_only_leaders'
        ])
        nat_troops = Pool(natname + '_troops', picks=[], merge=[
            natname + '_fort_troops',
            natname + '_nonfort_troops',
            natname + '_cap_only_troops'
        ])
        nat_fort = Pool(natname + '_fort', picks=[], merge=[
            natname + '_fort_leaders',
            natname + '_fort_troops'
        ])
        nat_nonfort = Pool(natname + '_nonfort', picks=[], merge=[
            natname + '_nonfort_leaders',
            natname + '_nonfort_troops'
        ])
        nat_coast = Pool(natname + '_coast', picks=[], merge=[
            natname + '_coast_leaders',
            natname + '_coast_troops'
        ])
        nat_all = Pool(natname + '_units', picks=[], merge=[
            natname + '_leaders',
            natname + '_troops'
        ])

        # Generate mage pool
        def get_mages(pool):
            return [unit.id
                    for unit in pool._picks.values()
                    if 'mage' in unit.tags]

        nat_fort_mages = Pool(natname + '_fort_mages', get_mages(nat_fort_l_pool))
        nat_nonfort_mages = Pool(natname + '_nonfort_mages', get_mages(nat_nonfort_l_pool))
        nat_coast_mages = Pool(natname + '_coast_mages', get_mages(nat_coast_l_pool))
        nat_cap_only_mages = Pool(natname + '_cap_only_mages', get_mages(nat_co_l_pool))
        nat_mages = Pool(natname + '_mages', merge=[
            nat_fort_mages.name,
            nat_nonfort_mages.name,
            nat_coast_mages.name,
            nat_cap_only_mages.name
        ])

        # Generate nonmage commanders
        def get_nonmages(pool):
            return [unit.id
                    for unit in pool._picks.values()
                    if not ('mage' in unit.tags)]
        nat_fort_commanders = Pool(natname + '_fort_commanders', get_nonmages(nat_fort_l_pool))
        nat_nonfort_commanders = Pool(natname + '_nonfort_commanders', get_nonmages(nat_nonfort_l_pool))
        nat_coast_commanders = Pool(natname + '_coast_commanders', get_nonmages(nat_coast_l_pool))
        nat_cap_only_commanders = Pool(natname + '_cap_only_commanders', get_nonmages(nat_co_l_pool))
        nat_commanders = Pool(natname + '_commanders', merge=[
            nat_fort_commanders.name,
            nat_nonfort_commanders.name,
            nat_coast_commanders.name,
            nat_cap_only_commanders.name
        ])

        # Get sacred units
        def get_sacreds(pool):
            return [unit.id
                    for unit in pool._picks.values()
                    if 'sacred' in unit.tags]

        nat_sacred_troops = Pool(natname + '_sacred_troops', get_sacreds(nat_troops))

        nation_pools += [
                nat_fort_l_pool,
                nat_fort_t_pool,
                nat_nonfort_l_pool,
                nat_nonfort_t_pool,
                nat_coast_l_pool,
                nat_coast_t_pool,
                nat_co_l_pool,
                nat_co_t_pool,
                nat_leaders,
                nat_troops,
                nat_fort,
                nat_nonfort,
                nat_sacred_troops,
                nat_fort_commanders,
                nat_nonfort_commanders,
                nat_coast_commanders,
                nat_cap_only_commanders,
                nat_commanders,
                nat_fort_mages,
                nat_nonfort_mages,
                nat_coast_mages,
                nat_cap_only_mages,
                nat_mages,
                nat_all
        ]

    eras = {'ea':'1', 'ma':'2', 'la':'3'}
    era_pools = []
    for era in eras:
        era_nat_leaders = [nat['file_name_base'] + '_leaders' for nat in nations_csv if nat['era'] == eras[era]]
        era_leaders_pool = Pool(era + '_leaders', picks=[], merge=era_nat_leaders)
        era_nat_troops = [nat['file_name_base'] + '_troops' for nat in nations_csv if nat['era'] == eras[era]]
        era_troops_pool = Pool(era + '_troops', picks=[], merge=era_nat_troops)
        era_nat_commanders = [nat['file_name_base'] + '_commanders' for nat in nations_csv if nat['era'] == eras[era]]
        era_commanders_pool = Pool(era + '_commanders', picks=[], merge=era_nat_commanders)
        era_nat_mages = [nat['file_name_base'] + '_mages' for nat in nations_csv if nat['era'] == eras[era]]
        era_mages_pool = Pool(era + '_mages', picks=[], merge=era_nat_mages)
        era_pools += [era_leaders_pool, era_troops_pool, era_commanders_pool, era_mages_pool]

    all_leaders = Pool('all_leaders', merge=['ea_leaders', 'ma_leaders', 'la_leaders'])
    all_troops = Pool('all_troops', merge=['ea_troops', 'ma_troops', 'la_troops'])
    all_commanders = Pool('all_commanders', merge=['ea_commanders', 'ma_commanders', 'la_commanders'])
    all_mages = Pool('all_mages', merge=['ea_mages', 'ma_mages', 'la_mages'])

    all_eras_pools = [all_leaders, all_troops, all_commanders, all_mages]


    with open(dir_root + '/data/1nation_units.yaml', 'w') as output:
        output.write(yaml.dump_all(nation_pools + era_pools + all_eras_pools))

if __name__ == "__main__":
    generate_nations()
    generate_units()
