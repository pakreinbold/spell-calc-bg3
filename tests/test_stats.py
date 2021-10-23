from math import comb
import numpy as np
from stats import (
    poly_coeff, distr_sdurv, dmg_distr, half_distr, adjusted_distr,
    get_stats
)


def test_poly_coeff():
    # Check recursion bounds
    assert poly_coeff(1, 1, -1) == 0
    assert poly_coeff(1, 1, 2) == 0
    assert poly_coeff(1, 0, 0) == 1

    # Check invalid inputs
    try:
        poly_coeff(-1, 1, 1)
    except ValueError:
        assert True
    try:
        poly_coeff(1, -1, 1)
    except ValueError:
        assert True

    # Check that it matches binomial for k=1
    for n in range(10):
        for q in range(n):
            assert poly_coeff(n + 1, 1, q) == comb(n + 1, q)


def test_distr_sdurv():
    # Check several examples
    for n in range(5):
        for k in range(5):
            y, p = distr_sdurv(n + 1, k + 1)

            # Check that the probability is normalized
            assert np.abs(p.sum() - 1) < 1e-10

            # Check that the outputs are the same length
            assert len(y) == len(p)


def test_dmg_distr():
    dmg, prb = dmg_distr('3d10', mod=4)

    # Check that the min/max damage is correct
    assert dmg.min() == 7
    assert dmg.max() == 34

    # Check that the probability is normalized
    assert np.abs(prb.sum() - 1) < 1e-10

    # Make sure that the outputs are the same size
    assert len(dmg) == len(prb)


def test_half_distr():
    dmg, prb = dmg_distr('3d8')
    hlf_dmg, hlf_prb = half_distr(dmg, prb)

    # Check that the min/max damage is correct
    assert hlf_dmg.min() == 1
    assert hlf_dmg.max() == 12

    # Check that the probability is normalized
    assert np.abs(hlf_prb.sum() - 1) < 1e-10

    # Make sure that the outputs are the same size
    assert len(hlf_dmg) == len(hlf_prb)

    # Make sure that all the abscissae are integers
    assert hlf_dmg.dtype == int

    # Make sure that there are no duplicate abscissae
    assert len(np.unique(hlf_dmg)) == len(hlf_dmg)

    # Make sure that the probabilities make sense
    assert np.all(hlf_prb >= 0)
    assert np.all(hlf_prb <= 1)


def test_adjusted_distr():
    # Check with half damage first
    damage, prob = adjusted_distr('2d10', hit_chance=0.75, half_damage=True)

    # Check that the damage bounds make sense
    assert damage.min() == 1
    assert damage.max() == 20

    # Check that the probability is normalized
    assert np.abs(prob.sum() - 1) < 1e-10

    # Check typing
    assert damage.dtype == int

    # Check with no half damage & modifier
    damage, prob = adjusted_distr('4d6', mod=3, hit_chance=0.9)

    # Check the bounds
    assert damage.min() == 0
    assert damage.max() == 27

    # Check that the pieces matchup
    assert np.abs(prob[0] - 0.1) < 1e-10
    assert np.abs(prob[1:].sum() - 0.9) < 1e-10

    # Check normalization
    assert np.abs(prob.sum() - 1) < 1e-10

    # Check the typing
    assert damage.dtype == int


def test_get_stats():
    # Make some mock data
    dmg = np.arange(1, 21)
    prb = 0.05 * np.ones(dmg.shape)

    # Call the tested-function
    ev, min7, min9, max7, max9 = get_stats(dmg, prb)

    # Check that the values are as expected
    assert np.abs(ev - 10.5) < 1e-10
    assert np.abs(min7 - 6) < 1e-10
    assert np.abs(min9 - 2) < 1e-10
    assert np.abs(max7 - 14) < 1e-10
    assert np.abs(max9 - 18) < 1e-10
