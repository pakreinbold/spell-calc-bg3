# %%
import matplotlib.pyplot as plt
from ipywidgets import interact
from damage_distribution import adjusted_distr
from spell_utility import load_cached_spells


def plot_dmg_distr(dice, modifier=0, hit_chance=1, half_damage=False):
    # Get distribution if it hits
    dmg, prb = adjusted_distr(dice, modifier, hit_chance=hit_chance, half_damage=half_damage)

    # Do the plotting
    plt.plot(dmg, prb, '-o')
    plt.ylim([0, 0.5])
    plt.xlabel('Damage')
    plt.ylabel('Probability')
    plt.xticks(dmg[::4], [int(x) for x in dmg[::4]])
    plt.title(
        f'''Dice Roll: {dice}
            Ability Modifier: {modifier}
            Hit Chance: {hit_chance}
            Half Damage: {half_damage}'''
    )
    plt.show()


def plot_spells(label='spells'):
    spells = load_cached_spells(label=label)
    spells = spells[~spells['Dice'].isna()]

    @interact(spell=spells['Name'].tolist(), hit_chance=(0, 1, 0.05))
    def plot_spell(spell, hit_chance):

        dice = spells[spells['Name'] == spell]['Dice'].iloc[0]
        half_damage = spells[spells['Name'] == spell]['Half Damage'].iloc[0]

        plot_dmg_distr(dice, hit_chance=hit_chance, half_damage=half_damage)
