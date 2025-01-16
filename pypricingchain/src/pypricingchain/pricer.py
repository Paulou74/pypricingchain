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




