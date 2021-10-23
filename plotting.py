# %%
import matplotlib.pyplot as plt
from ipywidgets import interact
from stats import adjusted_distr, get_stats
from utility import load_cached_spells


def plot_dmg_distr(dice, modifier=0, hit_chance=1, half_damage=False):
    # Get distribution if it hits
    dmg, prb = adjusted_distr(dice, modifier, hit_chance=hit_chance, half_damage=half_damage)

    # Get informative statistics
    med, min7, min9, max7, max9 = get_stats(dmg, prb)
    print(f'''
        DAMAGE STATS
        Expected Value: {med:.2f}
        70% Greater: {min7:.1f}
        90% Greater: {min9:.1f}
        70% Smaller: {max7:.1f}
        90% Smaller: {max9:.1f}
    ''')

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
    def plot_spell(spell, hit_chance=0.5):

        dice = spells[spells['Name'] == spell]['Dice'].iloc[0]
        half_damage = spells[spells['Name'] == spell]['Half Damage'].iloc[0]

        plot_dmg_distr(dice, hit_chance=hit_chance, half_damage=half_damage)
