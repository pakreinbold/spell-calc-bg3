from math import comb
import numpy as np
from damage_distribution import poly_coeff, distr_sdurv, dmg_distr


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
    dmg, prb = dmg_distr('3d10', 4)

    # Check that the min/max damage is correct
    assert dmg.min() == 7
    assert dmg.max() == 34

    # Check that the probability is normalized
    assert np.abs(prb.sum() - 1) < 1e-10

    # Make sure that the outputs are the same size
    assert len(dmg) == len(prb)
