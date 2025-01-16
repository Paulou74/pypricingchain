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
        Method that simulates the underlying path depending on the applied decrement
        
        """