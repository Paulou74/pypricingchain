import numpy as np


import logging
logging.basicConfig(level=logging.INFO)

# --------------------------------------------------------------------------
#  Class
# --------------------------------------------------------------------------

class Phoenix:

    # Class attributes
    underlying : list
    maturity : int
    coupon : float
    obs_per_year : int
    autocall_barrier : float
    coupon_barrier : float
    put_strike : float
    put_barrier : float
    n_obs : int

    arr_autocall_barriers : np.ndarray
    arr_coupon_barriers : np.ndarray

    decrement : float
    decrement_point : bool
    decrement_percentage : bool
    

    # Default constructor
    def __init__(self, underlying : list, maturity : int, coupon : float, obs_per_year : int, autocall_barrier : float, 
                 coupon_barrier : float, put_strike : float, put_barrier : float,
                 decrement : float, decrement_point : bool, decrement_percentage : bool):
        
        """
        Default constructor for Phoenix classes

        Args:
            
            :underlying list: List of underlyings.
            :maturity int: Maturity of the product.
            :obs_freq str: Observation frequency.
            :autocall_barrier float: Value of the autocall barrier.
            :coupon_barrier float: Value of the coupon barrier.
            :put_strike float: Value of the strike of the put at maturity.
            :put_barrier float: Value of the barrier of the put at maturity.
            :decrement float: Annual decrement.
            :decrement_point bool: Set to True for decrement in point.
            :decrement_percentage boo: Set to True for decrement in percentage.

        Returns:

            :phoenix Phoenix: Phoenix product

        """
        logging.info("Creating your product ...")
        # Check the validity of the inputs
        if len(underlying) != 2:
            raise ValueError("The underlying must consist of 2 underlyings.")
        if not all(isinstance(elem, str) for elem in underlying):
            raise ValueError("The list must contain tickers in the form of str.")
        
        if maturity <= 0:
            raise ValueError("Maturity cannot be negative!")
        
        if coupon < 0:
            raise ValueError("The coupon value cannot be negative!")
        
        if obs_per_year not in [12, 4, 2, 1]:
            raise ValueError("Number of observations not supported: only enter 12 (monthly), 4 (quarterly), 2 (semi-annually), 1 (annually) observations.")
        
        if autocall_barrier < 0:
            raise ValueError("Autocall barrier cannot be negative!")
        
        if coupon_barrier < 0:
            raise ValueError("Coupon barrier cannot be negative!")
        
        if put_strike < 0:
            raise ValueError("The Put's Strike cannot be negative!")
        
        if put_barrier < 0:
            raise ValueError("The Put's Barrier cannot be negative!")
        
        if decrement < 0:
            raise ValueError("The value of the decrement cannot be negative.")
        
        if decrement_point and decrement_percentage:
            raise ValueError("Cannot be point and percentage decrement at the same time. Please set one to False")
        
        # If all the inputs are valid, set the inputs to the class variables
        self.underlying = underlying
        self.maturity = maturity
        self.coupon = coupon
        self.obs_per_year = obs_per_year
        self.autocall_barrier = autocall_barrier
        self.coupon_barrier = coupon_barrier
        self.put_strike = put_strike
        self.put_barrier = put_barrier
        self.decrement = decrement
        self.decrement_point = decrement_point
        self.decrement_percentage = decrement_percentage

        # Compute the arrays + Assignement
        self.n_obs = self.obs_per_year * self.maturity
        arr_autocall = np.ones(self.n_obs) * self.autocall_barrier
        arr_coupon = np.ones(self.n_obs) * self.coupon_barrier
        self.arr_autocall_barriers = arr_autocall
        self.arr_coupon_barriers = arr_coupon
        logging.info("Product successfully created!")
