from pypricingchain.phoenix import Phoenix
from pypricingchain.pricer import Pricer
import numpy as np
import pytest

def test_pricer_input():

    phoenix = Phoenix(underlying = ["AAPL", "MSFT"],
    maturity=10,
    coupon=0.05/12,
    obs_per_year=12,
    autocall_barrier=1.0,
    coupon_barrier=0.8,
    put_strike=1.0,
    put_barrier=0.7,
    decrement=50,
    decrement_point=True,
    decrement_percentage=False)

    pricer = Pricer(25000, phoenix)
    price, mat_spots = pricer.price_from_inputs(np.array([0.03, 0.06]), np.array([0.03, 0.03]), np.array([0.25, 0.34]), 0.05, 0.05)

    assert 0.90 < price < 0.95
    assert mat_spots[0, 0] == 1000

def test_pricer_data():

    phoenix = Phoenix(underlying = ["AAPL", "MSFT"],
    maturity=10,
    coupon=0.05/12,
    obs_per_year=12,
    autocall_barrier=1.0,
    coupon_barrier=0.8,
    put_strike=1.0,
    put_barrier=0.7,
    decrement=50,
    decrement_point=True,
    decrement_percentage=False)

    pricer = Pricer(25000, phoenix)
    price, mat_spots = pricer.price_from_market_data(np.array([0.03, 0.06]), np.array([0.03, 0.03]), 0.05)

    assert isinstance(price, float)
    assert mat_spots[0, 0] == 1000