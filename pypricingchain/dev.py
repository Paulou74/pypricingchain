from pypricingchain.phoenix import Phoenix

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
print(my_phoenix)