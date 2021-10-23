import os
import glob
import pandas as pd
from pandas._testing import assert_frame_equal
from utility import (
    load_cached_spells, scrape_spells_fextralife, cache_spells, process_description
)


def list3(*args, **kwargs):
    return ['a', 'b', 'c']


def test_scrape_spells_fextralife(monkeypatch):
    # Check that the early access DataFrame is shorter
    spells_ea, spells_full = scrape_spells_fextralife()
    assert spells_ea.index.shape[0] < spells_full.index.shape[0]

    # Check that DataFrame lists not len()==2 are caught
    monkeypatch.setattr('pandas.read_html', list3)
    try:
        scrape_spells_fextralife()
        assert False  # fail if no ValueError raised
    except ValueError:
        assert True


def test_cache_and_load_spells():
    # Cache some mock DataFrame
    mock_df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    save_name = cache_spells(mock_df, label='mock')

    # Check that the DataFrame was saved to the cache
    assert save_name in [x.replace('\\', '/') for x in glob.glob('cache/*.csv')]

    # Check that the loaded cache is the same
    loaded_mock_df = load_cached_spells(label='mock')
    assert_frame_equal(mock_df, loaded_mock_df)

    # Remove the mock csv
    os.remove('cache/mock.csv')


def test_process_description():
    # Make some fake description
    description = 'Summon Yeeter McYeeterson to assail your foes ' \
        + 'for 3d20 penetrating damage. On a successful save, the creature only takes half ' \
        + 'damage. Attack/Save: Ranged Attack Range: 333m/999ft'

    # Process the description
    dice_roll, damage_type, attack_type, half_damage = process_description(description)

    # Check that the information is gathered correctly
    assert dice_roll == '3d20'
    assert damage_type == 'penetrating'
    assert attack_type == 'ranged'
    assert half_damage is True
