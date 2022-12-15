import pandas as pd
import numpy as np


# solver
from scipy.optimize import fsolve


class HoLee(object):

    '''
    Class to calibrate Binamial Tree to fit the interest rate
    using Ho Lee implementation
    ============================
    n: number of time period
    T: number of years.
    dt: T/n
    zcb: array, price of zero coupon bonds.
        Make sure these are ZCB. Only check is if zcb >1, then devide by 100.

    sigma = Annualised Volatility (standard deviation)

    =============================
    Assumption: dt is constant
    Future development ideas:
        If dt between each price not constant,
        implement raw interpolation

    '''

    def __init__(self, zcb, T,  sigma):

        self.zcb = np.array(zcb)  # Array
        self.n = len(self.zcb)
        self.T = T
        self.sigma = sigma  # Annualised volatility
        self.dt = T/self.n

        self.rates = np.zeros((self.n, self.n))
        self.thetas = np.nan  # store theta's value once calibrated

        # if ZCB > 1 ==> ZCB quoted per $100.
        if self.zcb[-1] > 1.0:
            self.zcb /= 100

        # Extract first interest rate (Trivial)
        self.rates[0, 0] = -np.log(self.zcb[0])/self.dt

        self.fit_theta()

        # Ideas, if dt not fixed, insert array along zcb to have time.

    @staticmethod
    def forward_tree(r0, sigma, dt, thetas):
        """
        Forward tree valuation
        Works for both Ho Lee and BDT model (change r_0 to ln r_0)

        Args:
            r0 (float): _description_
            sigma (float): _description_
            dt (float): _description_
            thetas (array / list): _description_

        Returns:
             nxn array: interest rates

        =========================
        Uses backward tree for Bond evaluation
        Future area of improvement, maybe use
        backward_tree method
        """
        n = len(thetas)
        tree_rate = np.zeros((n+1, n+1))
        tree_rate[0, 0] = r0
        tree_zcb = np.zeros((n+2, n+2))
        tree_zcb[:, -1] = 1.0  # Could be 100.0

        for i in range(n):
            tree_rate[0, i+1] = tree_rate[0, i] + thetas[i] * dt \
                + sigma * np.sqrt(dt)

            # Vectorise calculation by -2 sigma on each row
            # (column-wise operation)

            # ignore first row (already calculated)
            tree_rate[1:i+2, i+1] = tree_rate[0, i+1] \
                - 2 * np.arange(1, i+2) * sigma * np.sqrt(dt)

        # Calculate ZCB backward

        for i in np.arange(n, -1, -1):

            tree_zcb[0:i+1, i] = np.exp(-tree_rate[:i+1, i] * dt) \
                * 0.5 * (tree_zcb[0:i+1, i+1] + tree_zcb[1:i+2, i+1])

        return tree_rate, tree_zcb

    def fit_theta(self):
        """
        Find theta parameters
        -------------------------
        In financial mathematics, the Ho–Lee model is a short rate model widely used 
        in the pricing of bond options, swaptions and other interest rate derivatives,
        and in modeling future interest rates. It was developed in 1986 by Thomas Ho and Sang Bin Lee.
        (from Wikepedia: https://en.wikipedia.org/wiki/Ho%E2%80%93Lee_model)

        - Risk Neutral probability = 0.5

        Drawback: Ho-Lee model allows negative interest rate

        Great ressource: 
        https://www.bensblog.tech/fixed_income/HoLee_Model/
        """
        thetas = []

        r0 = self.rates[0, 0]

        for i in self.zcb[1:]:
            p0 = i
            func = (lambda t: self.forward_tree(
                r0, self.sigma, self.dt, thetas+[t])[1][0, 0]-p0)
            new_theta = fsolve(func, 0.001)
            thetas.append(new_theta[0])

        self.thetas = thetas
        self.rates = self.forward_tree(r0, self.sigma, self.dt, thetas)[0]


class BlackDermanToy(object):

    '''
    Class to calibrate Binamial Tree to fit the interest rate
    using  Black Derman Toy implementation
    ============================
    n: number of time period
    T: number of years. 
    dt: T/n
    zcb: array, price of zero coupon bonds. 

    sigma = vol of log interest rate!(standard deviation)

    =============================
    Assumption: dt is constant
    Future development ideas: 
        If dt between each price not constant, 
        implement raw interpolation  

    =============================

    '''

    def __init__(self, zcb, T,  sigma):

        self.zcb = np.array(zcb)  # Array
        self.n = len(self.zcb)
        self.T = T
        self.sigma = sigma  # vol of log interest rate!
        self.dt = T/self.n

        self.rates = np.zeros((self.n, self.n))
        self.thetas = np.nan  # store theta's value once calibrated

        # if ZCB > 1 ==> ZCB quoted per $100.
        if self.zcb[-1] > 1.0:
            self.zcb /= 100

        # Extract first interest rate (Trivial)
        self.rates[0, 0] = -np.log(self.zcb[0])/self.dt

        self.fit_theta()

    @staticmethod
    def forward_tree(r0, sigma, dt, thetas):
        """
        Forward tree valuation
        Args:
            r0 (float): _description_
            sigma (float): _description_
            dt (float): _description_
            thetas (array / list): _description_

        Returns:
             nxn array: interest rates

        =========================
        Uses backward tree for Bond evaluation
        Future area of improvement, maybe use
        backward_tree method
        """
        n = len(thetas)
        tree_rate = np.zeros((n+1, n+1))
        tree_rate[0, 0] = np.log(r0)
        tree_zcb = np.zeros((n+2, n+2))
        tree_zcb[:, -1] = 1.0  # Could be 100.0

        for i in range(n):
            tree_rate[0, i+1] = tree_rate[0, i] + thetas[i] * dt \
                + sigma * np.sqrt(dt)

            # Vectorise calculation by -2 sigma on each row
            # (column-wise operation)

            # ignore first row (already calculated)
            tree_rate[1:i+2, i+1] = tree_rate[0, i+1] \
                - 2 * np.arange(1, i+2) * sigma * np.sqrt(dt)

        # Calculate ZCB backward

        for i in np.arange(n, -1, -1):

            r = np.exp(tree_rate[:i+1, i])
            tree_zcb[0:i+1, i] = np.exp(-r * dt) \
                * 0.5 * (tree_zcb[0:i+1, i+1] + tree_zcb[1:i+2, i+1])

        # z_i = ln(r_i) <=> r_i = exp(z_i)
        # replace 1.0 by 0.0
        tree_rate = np.exp(tree_rate)
        for i in range(len(tree_rate)):
            tree_rate[i+1:, i] = 0

        return tree_rate, tree_zcb

    def fit_theta(self):
        """
        Find theta parameters
        -------------------------

        ----------------------------------
        Note that differently form the Ho-Lee model, now sigma is the
        vol of log-interest rates. 
        - z_i = log(r_i) 
        - Risk Neutral probability = 0.5
        ----------------------------------
        Drawback: 
         - No analytical solution

        Great ressource: 
        https://www.bensblog.tech/fixed_income/HoLee_Model/
        """
        thetas = []
        r0 = self.rates[0, 0]

        for i in self.zcb[1:]:
            p0 = i
            func = (lambda t: self.forward_tree(
                r0, self.sigma, self.dt, thetas+[t])[1][0, 0]-p0)
            new_theta = fsolve(func, .001)
            thetas.append(new_theta[0])

        self.thetas = thetas
        self.rates = self.forward_tree(r0, self.sigma, self.dt, thetas)[0]


class Option_IR:

    def __init__(self, rate_obj, T, n):
        ''' in case I need to write something'''

        self.T = T          # Years
        self.n = n          # n

        self.dt = T/n

        self.rate_obj = rate_obj
        self.zcb = rate_obj.zcb
        self.tree_rates = rate_obj.rates[:n+1, :n+1]  # no need for self here

        # Set fair swap rate
        self.c_swap = self._swap_rate()

    def cash_flow(self, c=np.nan, notional=100.0, otype="cap"):
        """
        Calculate Binomial tree for a cap
        c: swap rate (similar to Strike)
        cp str : cap/ floor flag (call/put equivalent)
        notional: (=N in the formula)
        return: tree cash flow
        """

        tree_ctns = self.ctns_rate(self.tree_rates, self.dt)

        # create an empty array for Cash-Flow tree
        tree_cf = np.zeros((self.n+1, self.n+1))
        if otype == "cap":
            tree_cf = self.dt * notional * np.maximum(tree_ctns - c, 0)

        elif otype == "floor":
            tree_cf = self.dt * notional * np.maximum(c - tree_ctns, 0)

        elif otype == "swap":
            tree_cf = self.dt * notional * (tree_ctns - c)

            for i in range(self.n):
                tree_cf[i+1:, i] = 0

        else:
            print("No option type inputed, \n Please choose:")
            print("1.cap \n 2. floor \n 3. swap")
            return
        return tree_cf

    def option(self, c, notional, otype="cap"):

        cash_flow = self.cash_flow(c, notional, otype)

        rates = self.tree_rates

        tree = self.backward_tree(cash_flow, rates, self.dt)

        return tree

    def fair_swap(self):

        return self.option(self.c_swap, 100, "swap")

    def swaption(self, t):

        a = self.fair_swap()

        a = a[:t+1, :t+1]
        a[:, -1] = np.where(a[:, -1]-self.c_swap > 0, a[:, -1], 0)

        tree = np.zeros((t+1, t+1))
        # intresic value
        tree[:, -1] = a[:, -1]

        p = 0.5
        for i in range(t, 0, -1):
            tree[:i, i-1] = np.exp(-self.tree_rates[:i, i-1] * self.dt) \
                * ((p * tree[:i, i] + (1-p) * tree[1:i+1, i]))

        return tree

    def _swap_rate(self):
        """
        Find Fair swap rate analytically
        pro: Analitical solution

        Args:
            zcb (list / array): zero coupon bond

        Returns:
            float: fair swap rate

        ===========================================
        NB: I could create a bigger object so I don't have
        to manually input the zcb array. Alternatively, 
        I could calculate the ZCB from the array.  
        """

        k = len(self.tree_rates)

        self.c_swap = 1/self.dt * (1-self.zcb[k-1]) / (sum(self.zcb[:k]))

        return self.c_swap

    def fit_swap_rate(self):
        """
        Depreciated: 
        _swap_rate() is now used at instantiation
        Could still be useful on some occasions, 
        but will be ignored for now
        ---------------------------------------------
        Find fair swap rate using a numerical method. 
        Pro: no zcb needed
        Con: Not an analytical solution

        Returns:
            float: fair swap rate
        """

        # Notional amount is irrelevant
        func = (lambda t: self.option(t, 1.0, "swap")[0, 0])
        c = fsolve(func, 0.001)
        self.swap_rate = c[0]
        return c[0]

    @staticmethod
    def backward_tree(tree_cf, tree_rates, dt):
        """
        Calculate whole tree backward
        ==============================
        Args:
            tree_cf (nxn np.array): Cash Flow
            tree_rates (nxn np.array): rates from Ho Lee or Black Derman Toy
            dt (float): time step (assume constant)

        Returns:
            _type_: _description_
        """
        n = len(tree_rates)
        p = 0.5  # probability

        tree_eu = np.zeros((n, n))

        # intresic value
        tree_eu[:, -1] = np.exp(-tree_rates[:, -1] * dt) * tree_cf[:, -1]

        for i in range(n-1, 0, -1):
            tree_eu[:i, i-1] = np.exp(-tree_rates[:i, i-1] * dt) \
                * ((p * tree_eu[:i, i] + (1-p) * tree_eu[1:i+1, i])
                    + tree_cf[:i, i-1])

        return tree_eu

    @staticmethod
    def ctns_rate(rate, time):

        return (np.exp(rate * time)-1) / time
