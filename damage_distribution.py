'''
The following analytical results were largely based on the paper:

Caiado, Camila CS, and Pushpa N. Rathie. "Polynomial coefficients and distribution of the
    sum of discrete uniform variables." In Eighth Annual Conference of the Society of Special
    Functions and their Applications, Pala, India, Society for Special Functions and their
    Applications. 2007.
'''
from math import floor, comb
import numpy as np


def poly_coeff(n, k, q):
    '''
    Returns the Polynomial Coefficient (PC), defined as the coefficient for x^q resultant from the
    expression
        (1 + x + ... + x^k)^n.

    Args:
        n (int): The outer exponent; n >= 0
        q (int): The identifying exponent for the term we want the coefficient for
            0 <= q <= n*k
        k (int): The max inner exponent; k >= 0

    Returns:
        (int): The polynomial coefficient
    '''
    if n < 0 or k < 0:
        raise ValueError('Recieved negative inputs.')

    # Check recursion bounds
    if q < 0 or q > (n * k):
        return 0
    elif q == 0 and k == 0:
        return 1

    # Compute recursive loop(s)
    res = 0
    for p in range(floor(q * (k - 1) / k) + 1):
        res += comb(n, q - p) * poly_coeff(q - p, k - 1, p)

    return res


def distr_sdurv(n, k):
    '''
    Returns the probability distribution of a Sum of Discrete Uniform Random Variables (sdurv). Let
        X = (X_1, X_2, ..., X_n)
    be a sample of random variables each drawn from a discrete uniform distribution on
    {0, 1, ..., k}. Define
        Y = X_1 + X_2 + ... + X_n.
    Then the distribution of Y is given by
        P(Y=y) = poly_coeff(n, k, y) / (k + 1)^n

    Args:
        n (int): Number of discrete uniform random variables to sum.
        k (int): Size of space each discrete uniform random variable can draw from.

    Returns:
        (np.array): y
        (np.array): P(Y=y)
    '''
    # All possibilities for y
    y = np.arange(0, n * k + 1)

    # Compute each option
    p = np.array([poly_coeff(n, k, y_) / (k + 1)**n for y_ in y])
    return y, p


def dmg_distr(dice, mod):
    '''
    Returns the damage distribution of a spell/ability assuming that it hits the target.

    Args:
        dice (str): Of the format "XdY", where X is the number of dice, and Y is the dice size.
        mod (int): Number added to the dice roll

    Returns:
        (np.array): Damage outcome
        (np.array): Probability of damage outcome
    '''
    # Decode the dice input
    n, k = [int(x) for x in dice.split('d')]

    # Get the distribution
    dmg, prb = distr_sdurv(n, k - 1)

    # Shift the damage & apply modifier
    dmg += n + mod

    return dmg, prb
