"""
Class object to store all Options parameters.
"""

class Parameters:
    """
    Object containing all parameter for option pricing
    """
    def __init__(self, stock, strike, t, T, rate, dividend, vol):
        """
        Parameters:
        ===========
            stock:          Initial stock price (at time = 0)
            strike:         Strike Price
            t:              Startint time: 0 ==> now , 1==> in 1 year time
            T:              Expiry date
            r:              Risk free rate
            dividend:       Dividient yield
            vol:            Volatility
        """

        self.stock    = float(stock)                    # Initial Stock price
        self.strike   = float(strike)                   # Strike Price
        self.t        = float(t)                        # Starting time:
                                                        # e.g. 0 ==> now , 1==> in 1 year time
        self.T        = float(T)                        # Expiry date.
        self.tau      = self.T - self.t                 # Time to Maturity
        self.rate     = float(rate)                     # Risk free rate
        self.dividend = float(dividend)                 # Dividend yield
        self.vol      = float(vol)                      # Volatility

    def get_attribute(self):
        """
        Prints all attribute of object
        """

        for i in (vars(self)):
            print("{0:10}: {1}".format(i, vars(self)[i]))
