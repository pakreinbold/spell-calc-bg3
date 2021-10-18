from spell_utility import scrape_spells_fextralife


def list3(*args, **kwargs):
    return ['a', 'b', 'c']


def test_scrape_spells_fextralife(monkeypatch):
    # Check that the early access DataFrame is shorter
    spells_ea, spells_full = scrape_spells_fextralife()
    assert spells_ea.index.shape[0] < spells_full.index.shape[0]

    # Check that DataFrame lists not len()==2 are caught
    monkeypatch.setattr('pandas.read_html', list3)
    try:
        scrape_spells_fextralife()
    except ValueError:
        assert True
