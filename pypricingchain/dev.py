import datetime
from datetime import datetime as dt
from datetime import timedelta
from pypricingchain.phoenix import Phoenix, Metrics
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
print(my_phoenix.underlying)

window=360
met = my_phoenix.compute_components_moments(window)
# print((dt.today() - timedelta(days=360)).strftime("%Y-%m-%d"))
# df_prices = get_stocks_data(my_phoenix.underlying, (dt.today() - timedelta(days=window)).strftime("%Y-%m-%d"), dt.today().strftime("%Y-%m-%d"))
# info_set = Information(
#     s = timedelta(days=window),
#     data_module=DataModule(df_prices),
#     time_column="Date",
#     company_column="ticker",
#     adj_close_column="Adj Close"
# )

# met = Metrics(
#     s = timedelta(days=window),
#     data_module=DataModule(df_prices),
#     time_column="Date",
#     company_column="ticker",
#     adj_close_column="Adj Close"
# ).compute_information(dt.today())

print(met)