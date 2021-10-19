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
    spells.to_csv(save_name)

    return save_name
