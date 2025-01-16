import numpy as np
import datetime
import matplotlib.pyplot as plt
from datetime import datetime as dt
from datetime import timedelta
from pypricingchain.phoenix import Phoenix, Metrics
from pypricingchain.pricer import Pricer
from pybacktestchain.data_module import DataModule, FirstTwoMoments, Information, get_stocks_data

dict_params = {
    "underlying" : ["AAPL", "MSFT"],
    "maturity": 10,
    "coupon": 0.05/12,
    "obs_per_year": 12,
    "autocall_barrier": 1.0,
    "coupon_barrier": 0.8,
    "put_strike": 1.0,
    "put_barrier": 0.7,
    "decrement": 50,
    "decrement_point": True,
    "decrement_percentage": False
}

my_phoenix = Phoenix(**dict_params)
pricer = Pricer(50000, my_phoenix)
window=360
price, mat = pricer.price_from_market_data(np.array([0.02, 0.03]), np.array([0.05, 0.03]), 0.03)
# price, mat = pricer.price_from_inputs(np.array([0.03, 0.06]), np.array([0.03, 0.03]), np.array([0.25, 0.34]), 0.05, 0.05)
print(price)
print(isinstance(price, float))
print(mat[0, :])
# met = my_phoenix.compute_components_moments(window)
# print(met)
# print(met["Ann. Volatility"].loc["AAPL"])

# mat_spots = pricer.generate_brownians([0.05, 0.05], [0.2, 0.2], 0.5)
# mat_undl = pricer.simulate_underlying_path(mat_spots)
# price = pricer.price_phoenix(mat_undl, 0.03)
# print(price)