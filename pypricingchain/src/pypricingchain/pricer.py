import pandas as pd
import numpy as np
import logging
from scipy.stats import norm

from pypricingchain.phoenix import Phoenix

logging.basicConfig(level=logging.INFO)



# --------------------------------------------------------------------------
#  Class
# --------------------------------------------------------------------------

class Pricer:

    # Class attributes
    n_sim : int
    phoenix : Phoenix

    # Default constructor
    def __init__(self, n_sim : int, phoenix : Phoenix):

        """
        Default constructor

        Args:

            :n_sim int: Number of paths to simulate.
            :n_steps int: Number of time steps.
        """ 

        if not isinstance(n_sim, int):
            raise ValueError(f"Incorrect type! Expected int and got {type(n_sim)}")
        
        self.n_sim = n_sim
        self.phoenix = phoenix
        logging.info("Pricer initialised")


    # Method to generate the brownians - Using extended Black-Scholes framework
    def generate_brownians(self, drifts : np.ndarray, diffusions : np.ndarray, correl : float):
        
        """
        Method that generates brownians corresponding the underlying assets randomness at each evaluation date.

        Args:

            :drifts np.ndarray: (2 x 1) Array containing the drift coefficients of each components.
            :diffusions np.ndarray: (2 x 1) Array containing the diffusion coefficients of each components.
            :correl float: Correlation between the returns of the 2 assets.
            :dt float: Size of the time step.

        Returns:

            :mat_spots np.ndarray: 3-dimensional matrix containing the simulated paths

        """

        # Generate the matrices of correlated brownian motions
        n_steps = self.phoenix.maturity * 360
        dt = 1/360                          # One day time step
        w_a = np.random.normal(0, 1, size=(n_steps, self.n_sim))
        w_orth = np.random.normal(0, 1, size=(n_steps, self.n_sim))
        w_b = correl * w_a + np.sqrt(1 - correl) * w_orth

        # Spot expressed in base 100
        mat_spots = np.zeros((n_steps + 1, self.n_sim, 2))
        mat_spots[0, :, :] = 100

        # Updating the simulated paths
        for t in range(1, n_steps + 1):

            # Update simulations for stock 1
            mat_spots[t, :, 0] = mat_spots[t-1, :, 0] * np.exp( 
                (drifts[0] - 0.5 * diffusions[0] ** 2) * dt + diffusions[0] * np.sqrt(dt) * w_a[t-1, :] 
            )

            # Update for simulations for stocks 2
            mat_spots[t, :, 1] = mat_spots[t-1, :, 1] * np.exp( 
                (drifts[0] - 0.5 * diffusions[0] ** 2) * dt + diffusions[0] * np.sqrt(dt) * w_b[t-1, :] 
            )

        return mat_spots
    
    
    def simulate_underlying_path(self, mat_spots : np.ndarray):

        """
        Method that simulates the underlying path depending on the applied decrement.

        Args:

            :mat_spots np.ndarray: Matrix containing the simulated spots trajectories

        Returns:

            :mat_underlying np.ndarray: 2-dimensional array containing the simulated paths of the underlying 

        """

        # Generating the matrix of simulated paths
        n_steps = self.phoenix.maturity * 360
        mat_underlying = np.zeros((n_steps + 1, self.n_sim))
        mat_underlying[0, :] = 1000

        # Compute the returns of the components
        mat_ret_compo = np.diff(mat_spots, axis=0) / mat_spots[:-1, :, :]
        
        # If a decrement needs to be applied
        if self.phoenix.decrement != 0 and (self.phoenix.decrement_percentage or self.phoenix.decrement_point):
            
            # Applying decrement in percentage
            if self.phoenix.decrement_percentage:

                for t in range(n_steps):
                    
                    # Compute the average return of both assets
                    arr_ret = 0.5 * mat_ret_compo[t, :, 0] + 0.5 * mat_ret_compo[t, :, 1]
                    mat_underlying[t + 1, :] = mat_underlying[t, :] * (1 + arr_ret - self.phoenix.decrement / 360)

            # Applying decrement in points
            if self.phoenix.decrement_point:

                for t in range(n_steps):

                    # Compute the average return of both assets
                    arr_ret = 0.5 * mat_ret_compo[t, :, 0] + 0.5 * mat_ret_compo[t, :, 1]
                    mat_underlying[t + 1, :] = mat_underlying[t, :] * (1 + arr_ret) - self.phoenix.decrement / 360
        else:

            # Case no decrement need to be applied
            for t in range(n_steps):
                    
                # Compute the average return of both assets
                arr_ret = 0.5 * mat_ret_compo[t, :, 0] + 0.5 * mat_ret_compo[t, :, 1]
                mat_underlying[t + 1, :] = mat_underlying[t, :] * (1 + arr_ret)


        return mat_underlying
    

    def price_phoenix(self, mat_underlying : np.ndarray, rf : float):
        
        """
        Method to price the Phoenix.

        Args:

            :mat_underlying np.ndarray: Matrix containing the simulated paths.
            :rf float: Risk free rate used for the discount

        Returns:

            :price float: Price of the structure

        """

        # Retrieve the data from the product for improved-readibility
        coupon = self.phoenix.coupon
        obs_per_year = self.phoenix.obs_per_year
        arr_autocall_barriers = self.phoenix.arr_autocall_barriers
        arr_coupon_barriers = self.phoenix.arr_coupon_barriers
        put_strike = self.phoenix.put_strike
        put_barrier = self.phoenix.put_barrier
        n_obs = self.phoenix.n_obs
        mat_flow = np.zeros((n_obs, self.n_sim))

        # Write the underlying in terms of performance
        mat_underlying = mat_underlying / mat_underlying[0, :]
        # Defined the discount factor
        time_step = int(360 / obs_per_year)
        arr_discount = [np.exp(-rf * (1 + i) * time_step / 360) for i in range(n_obs)]

        # Iterate over the observations periods
        arr_has_autocalled = np.ones(self.n_sim)
        for i in range(1, n_obs):

            # Scenario at maturity
            if i == n_obs:

                # Determine if the Coupon condition has been met
                arr_coupon = np.where(arr_obs > arr_coupon_barriers[i-1])[0]

                # Put condition
                arr_put = np.where(arr_obs < put_barrier)[0]
                put_payoff = np.maximum(put_strike - arr_obs[arr_put], 0)
                mat_flow[i-1, [arr_put]] = put_payoff * (arr_has_autocalled[arr_put] - 1)

                # Update cash flow matrix
                mat_flow[i-1, :] += 1
                mat_flow[i-1, [arr_coupon]] += coupon
                mat_flow[i-1, [arr_put]] = put_payoff * (arr_has_autocalled[arr_put] - 1)

            # Determine Autocall condition first
            idx = i * time_step
            arr_obs = mat_underlying[idx, :]
            arr_autocall = np.where(arr_obs > arr_autocall_barriers[i-1])[0]
            
            # Determine if the Coupon condition has been met
            arr_coupon = np.where(arr_obs > arr_coupon_barriers[i-1])[0]

            # Update the products cashflows accordingly
            mat_flow[i-1, [arr_coupon]] += coupon * arr_has_autocalled[arr_coupon]
            mat_flow[i-1, [arr_autocall]] += 1 * arr_has_autocalled[arr_autocall]

            # Discount the cashflows
            mat_flow[i-1, :] *= arr_discount[i-1]

            # Update the autocall condition 
            arr_has_autocalled[arr_autocall] = np.minimum(arr_has_autocalled[arr_autocall], 0)


        # Take the average value and return the price
        arr_price = mat_flow.sum(axis=0)

        return arr_price.mean()
    
    def price_from_inputs(self, arr_divs : np.ndarray, arr_rf : np.ndarray, arr_vol : np.ndarray, correl : float, disc_rate : float):

        """
        Method to price using the user's inputs.

        Args

            :arr_divs np.ndarray: Array containing the dividend yields.
            :arr_rf np.ndarray: Array containing the risk free rates.
            :arr_vol np.ndarray: Arary containing the assets volatilities.
            :correl float: Correlation between the component's returns.
            :disc_rate float: Discount rate to be used for the pricing.
        
        Returns

            :price float: Price of the structure.
            :mat_underlying np.ndarray: Matrix containing the simulated paths.

        """

        # Simulated the paths
        arr_drifts = arr_divs + arr_rf
        mat_spots = self.generate_brownians(arr_drifts, arr_vol, correl)
        mat_underlying = self.simulate_underlying_path(mat_spots)

        # Price and return the outputs
        price = self.price_phoenix(mat_underlying, disc_rate)

        return price, mat_underlying


    
    
    def price_from_market_data(self, arr_divs : np.ndarray, arr_rf : np.ndarray, disc_rate : float):

        """
        Method to price using market data metrics as pricing input. To be used for illiquid assets where no forward data is available.

        Args:

            :arr_divs np.ndarray: Array containing the dividend yields of the underlings.
            :arr_rf np.ndarray: Array containing the risk free rates associated to each asset.
            :disc_rate float: Risk free rate used for the price discounting.

        Returns:

            :price float: Price of the structure.
            :mat_underlying np.ndarray: Matrix containing the simulated paths.

        """

        # Retrieve estimators of the volatilies and correlation using past data
        dict_metrics = self.phoenix.compute_components_moments(360)
        sigma_asset_1 = dict_metrics["Ann. Volatility"].loc[self.phoenix.underlying[0]]
        sigma_asset_2 = dict_metrics["Ann. Volatility"].loc[self.phoenix.underlying[1]]
        correl = dict_metrics["Ann. Correlation"].iloc[1, 0]

        # Simulate the assets path using this data
        arr_drifts = arr_rf - arr_divs 
        arr_diffusions = np.array([sigma_asset_1, sigma_asset_2])
        mat_spots = self.generate_brownians(arr_drifts, arr_diffusions, correl)
        mat_underlying = self.simulate_underlying_path(mat_spots)

        # Price
        price = self.price_phoenix(mat_underlying, disc_rate)

        return price, mat_underlying
