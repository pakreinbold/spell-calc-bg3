# Baldur's Gate 3 Spell Calculator
Provide an interface to compare different Baldur's Gate 3/5 Edition spells

## Damage Probability Distributions
The probability distribution of a given dice roll is calculated analytically as the sum of discrete uniform random variables, as in [Caiado & Rathie (2000)](https://www.researchgate.net/publication/228457326_Polynomial_coefficients_and_distribution_of_the_sum_of_discrete_uniform_variables). This is used as a base to compute the final damage distribution, which factors in whether or not the spell hit, ability modifiers, and whether the spell will do half damage if the target passes its saving throw. Below highlights the functionality of `plotting.plot_spells()` for early-access spells scraped and processed. You can select your spell, and adjust the hit chance to see what the probability distribution for the damage would look like. NOTE: spell description processing not finalized; spell damage not always accurate.

![Alt text](/screenshots/interactive_spell_plot.png?raw=true "Optional Title")

## Scraping Spell Lists
A list of all Baldur's Gate 3 spells can be found at [Fextralife's Spell List](https://baldursgate3.wiki.fextralife.com/Spells), which is easy to scrape (if you can call it that) since it's already in table format. All one needs do is `pd.read_html()`. After acquiring the table of spells once, it can be cached for later use. The following is the cached early-access spells acquired and cached in this way.

![Early-access Spells](/screenshots/spells_ea.png?raw=true "Early-access Spells")

As can be seen, the actual damage rolls (and how they scale with level) need to be harvested from the descriptions. However, important information about the spells is hidden within the scraped description. Thus, a processing script is necessary which takes something like the following (for Arms of Hadar)

> "2d6 NecroticCall forth tendrils of dark energy. Targets take 2d6 Necrotic and can't take reactions.On a successful save, targets only take half damage. Attack/Save: Strength Range: 3m/10ft"

and returns damage roll: "2d6", damage type: "necrotic", saving throw: "strength", half damage: "True".
