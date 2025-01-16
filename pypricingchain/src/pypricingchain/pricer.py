import pandas as pd
import numpy as np
import logging

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

        if isinstance(n_sim, int):
            raise ValueError(f"Incorrect typ! Expected int and got {type(n_sim)}")
        
        if isinstance(n_steps, int):
            raise ValueError(f"Incorrect typ! Expected int and got {type(n_steps)}")
        
        self.n_sim = n_sim
        self.phoenix = phoenix
        logging.info("Pricer initialised")

