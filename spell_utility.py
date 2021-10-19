# %%
import pandas as pd


def scrape_spells_fextralife():
    '''
    Scrape online resources to get available spells

    Returns:
        (pd.DataFrame): Spells available in early-access
            keys: Name, Level, School, Casting Time, Description, Classes
        (pd.DataFrame): All spells inferred from 5th-edition
            keys: Spell, Lvl, School, Casting Time, Concentration, Description, Classes

    Raises:
        ValueError: If the more/less than 2 tables are found on the website.
    '''
    # Website to get spells from
    url = 'https://baldursgate3.wiki.fextralife.com/Spells'

    # List of dataframes; tables directly on website
    dfs = pd.read_html(url)

    # Check that returned tables are as expected
    if len(dfs) != 2:
        raise ValueError(f'Expected two DataFrames from {url}, but there were {len(dfs)}')
    else:
        # Sort tables based on n_rows; shortest to longest
        dfs = sorted(dfs, key=lambda x: x.index.shape[0])

        # Longer table is full spell list, shorter is Early-access
        spells_ea = dfs[0]
        spells_full = dfs[1]

    return spells_ea, spells_full


def cache_spells(spells, label='spells'):
    '''
    Store the spells in a .csv file, so that they don't have to be scraped.

    Args:
        spells (pd.DataFrame): Table that contains spells and their relevant information
        label (str): What to include in the save-name
    '''
    save_name = f'cache/{label}.csv'
    spells.to_csv(save_name, index=False)

    return save_name


def load_cached_spells(label='spells'):
    '''
    Load the labeled spells from the cache.

    Args:
        label (str): The identifying part of the filename

    Returns:
        (pd.DataFrame): The table containg the spells, their descriptions, etc.
    '''
    # Get the DataFrame from the cache
    file_name = f'cache/{label}.csv'
    spells = pd.read_csv(file_name)

    return spells


def process_description(description):
    '''
    Find how much damage a spell does, whether it's a ranged attack or has a saving throw, whether
    it deals half-damage if the enemy saves, what type of damage it is (fire, thunder, etc.), what
    the saving ability is (strength, constitution, etc.), what ability score the spell recieves
    modifying damage from, etc.

    Args:
        description (str): The full description of the spells effect

    Returns:
        (str): Should be of the form "XdY" if the spell does damage, or None if it is not a
            damage-dealing spell.
        (str): Type of spell; should be "Ranged Attack" or "Saving Throw"
        (bool): Whether or not the spell does half-damage even if the enemy saves
        (str): Damage type (e.g., fire, thunder, frost, piercing, etc.)
        (str): Saving ability (e.g., constitution, charisma, etc.)
        (str): Modifying ability (e.g., wisdom, intelligence, etc.)
    '''
    # TODO: Use key-words "deals", "takes" to distinguish damage dealing spells from heals
    # TODO: Use regex to search for "XdY" pattern
    # TODO: Use regex to find 'half-damage'
    # TODO: Search for damage type key-words
