# %%
import matplotlib.pyplot as plt
from damage_distribution import dmg_distr

dmg, prb = dmg_distr('6d4', 3)
plt.plot(dmg, prb, '-o')
plt.xlabel('Damage')
plt.ylabel('Probability')
plt.show()
