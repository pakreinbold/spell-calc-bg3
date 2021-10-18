# %%
import matplotlib.pyplot as plt
from damage_distribution import dmg_distr

dmg, prb = dmg_distr('3d10', 0)
plt.plot(dmg, prb, '-o')
plt.xlabel('Damage')
plt.ylabel('Probability')
plt.xticks(dmg[::4], [int(x) for x in dmg[::4]])
plt.show()
