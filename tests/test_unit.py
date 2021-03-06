from domydrafter.data import unit
Unit = unit.Unit

fir_bolg_druid_csv = {
        'id': 2469,
        'name': 'Fir Bolg Druid',
        'A': 1,
        'rand1': 100,
        'nbr1': 1,
        'mask1': 9728,
        'holy': None
    }

fir_bolg_druid_final_attr = {
    'paths': {
        'A': 1,
        'random': [
            (100, ['W', 'E', 'N'], 1)
        ]
    }
}

fir_bolg_druid_final_tags = ['mage']

firbold_druid_final_unit = Unit(2469, 'Fir Bolg Druid', fir_bolg_druid_final_attr, fir_bolg_druid_final_tags)


militia_csv = {
    'id': 1001,
    'name': 'milita',
}

def test_decode_paths_mask():
    mask = 9728
    expected = ['W', 'E', 'N']
    assert unit.decode_paths_mask(mask) == expected


def test_process_paths_data():
    expected = {
        'A': 1,
        'random': [
            (100, ['W', 'E', 'N'], 1)
        ]
    }
    paths_data = unit.process_paths_data(fir_bolg_druid_csv)
    assert paths_data == expected


def test_process_paths_data_no_paths():
    expected = dict()
    paths_data = unit.process_paths_data(militia_csv)
    assert paths_data == expected


def test_get_paths():
    expected = {
        'A': 1,
        'random': [
            (100, ['W', 'E', 'N'], 1)
        ]
    }
    paths = unit.get_paths(fir_bolg_druid_csv)
    assert paths == expected


def test_unit_pipeline():
    assert unit.unit_pipeline(fir_bolg_druid_csv) == firbold_druid_final_unit