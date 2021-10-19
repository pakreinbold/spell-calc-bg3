# Baldur's Gate 3 Spell Calculator
Provide an interface to compare different Baldur's Gate 3/5 Edition spells

## Damage Probability Distributions
The probability distributions of a given dice roll are calculated analytically as the sum of discrete uniform random variables. For example, the outcomes of 3 10-sided dice (3d10) is shown below.


![Alt text](/screenshots/3d10.png?raw=true "Optional Title")

## Scraping Spell Lists
A list of all Baldur's Gate 3 spells can be found at [Fextralife's Spell List](https://baldursgate3.wiki.fextralife.com/Spells), which is easy to scrape (if you can call it that) since it's already in table format. All one needs do is `pd.read_html()`. After acquiring the table of spells once, it can be cached for later use. The following is the cached early-access spells acquired and cached in this way.

![Early-access Spells](/screenshots/spells_ea.png?raw=true "Early-access Spells")

As can be seen, the actual damage rolls (and how they scale with level) need to be harvested from the descriptions.
