# %%
import pandas as pd
import re


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
    # TODO: Use regex to find 'half-damage'

    # Initialize
    dice_roll = None
    damage_type = None
    attack_type = None
    half_damage = False

    # Convert to lower-case for easier processing
    txt = description.lower()

    # If match XdY ZZZ pattern, return list of matches; else, None
    dice_pat = re.findall('[0-9]*d[0-9]+ [a-z]+', txt)
    if len(dice_pat) > 0:

        # If only one match, take first
        if len(dice_pat) == 1:
            dice_pat = dice_pat[0].split()

        # Ignore first match, since it has strange typing
        else:
            dice_pat = dice_pat[1].split()

        dice_roll = dice_pat[0]
        damage_type = dice_pat[1]

    # Search for the attack type
    att_pat = re.findall('attack/save: [a-z]+', txt)
    if len(att_pat) > 0:

        # If a match is found, need to remove 'attack/save:' from it
        attack_type = att_pat[0].split(': ')[1]

    # Search for "half damage"
    half_pat = re.findall('half damage', txt)
    if len(half_pat) > 0:
        half_damage = True

    return dice_roll, damage_type, attack_type, half_damage
