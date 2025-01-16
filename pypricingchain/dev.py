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
    "coupon": 0.05,
    "obs_per_year": 12,
    "autocall_barrier": 1.0,
    "coupon_barrier": 0.8,
    "put_strike": 1.0,
    "put_barrier": 0.7,
    "decrement": 0.05,
    "decrement_point": False,
    "decrement_percentage": True
}

my_phoenix = Phoenix(**dict_params)
pricer = Pricer(1000, my_phoenix)
mat_spots = pricer.generate_brownians([0.05, 0.05], [0.2, 0.2], 0.5)
window=360
met = my_phoenix.compute_components_moments(window)
print(met)

plt.plot(mat_spots[:,:, 1])
plt.show()