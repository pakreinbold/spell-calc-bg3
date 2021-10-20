# %%
import matplotlib.pyplot as plt
from damage_distribution import adjusted_distr


def plot_dmg_distr(dice, modifier=0, hit_chance=1, half_damage=False):
    # Get distribution if it hits
    dmg, prb = adjusted_distr(dice, modifier, hit_chance=hit_chance, half_damage=half_damage)

    # Do the plotting
    plt.plot(dmg, prb, '-o')
    plt.xlabel('Damage')
    plt.ylabel('Probability')
    plt.xticks(dmg[::4], [int(x) for x in dmg[::4]])
    plt.show()
