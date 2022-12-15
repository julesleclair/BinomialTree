import numpy as np

class BinomialTree:
    """
    Class Binomial tree.
    By default use CRR methodology

    --------------------------------
    Note:
        if Volatility paramter is given, u and d are calculated
        automatically.
        if instead parameter u and d are given,
        you can upload directly into the object as:
        obj = Tree(param, n)
        obj.u = 1.2
        obj.d = 1/1.2

    Future Idea:
    To use the Binomial Asset Pricing Model as per Steven E. Shreve
    book's Stochastic Calculos for Finance I:
    use obj.set_apm(u, d),
    where u and d have to be manually inputed.
    """

    def __init__(self, param, n):
        self.param = param      # Parameter object
        self.n = n              # number of timestep

        self.dt = self.param.tau / self.n

        self.u = 0 # up movement
        self.d = 0 # down movement

        self.p = 0 # probability

        self.t_stock = np.zeros((n+1,n+1))

        # set European and Amerian option
        self.t_eu_c = 0
        self.t_eu_p = 0
        self.t_am_c = 0
        self.t_am_p = 0


        self.set_crr() # By default using the CRR model

    def set_crr(self):
        """
        Set parameter according to the Cox, Ross and Rubinstein (1979) model
        """

        self.u = np.exp(self.param.vol * np.sqrt(self.dt)) # up
        self.d = 1/self.u # down (faster)

        self.p = (np.exp(self.param.rate * self.dt) - self.d) / (self.u - self.d)

    def set_apm(self, u, d):
        """
        Set parameter according the The Binomial Asset Pricing Model
        Steven E. Schreve
        Stochastic Calculus for Finance 1: The Binomial Asset Pricing Model
        """
        self.u = u
        self.d = d
        self.p = (1 + self.param.rate - self.d) / (self.u - self.d)

    def set_tree(self):
        """
        Summary:
            Calculate Binomial Tree using CRR method
        Comment:
            - Faster version. Instead of using a double loop,
              you can vectorise one of the loop
            - For european option pricing,
              only Terminal Stock price required.
        """
        for i in range(self.n+1):
            self.t_stock[:i+1,i:i+1] = (self.param.stock * self.u**(np.arange(i,-1,-1)) \
                * self.d**(np.arange(0,i+1,1))).reshape(-1,1)

        return


    def set_european(self):
        """
        Set European Call and Put option
        """
        self.t_stock[:,-1] = (self.param.stock * self.u**(np.arange(self.n, -1, -1)) \
                * self.d**(np.arange(0,self.n + 1, 1)))

        self.t_eu_c = self.t_stock.copy()
        self.t_eu_p = self.t_stock.copy()

        #Intrinsic option price at the final node
        self.t_eu_c[:,-1] =  np.maximum(self.t_eu_c[:,-1] \
            - self.param.strike, 0.0) # call

        self.t_eu_p[:,-1] =  np.maximum(self.param.strike \
            - self.t_eu_p[:,-1], 0.0) # put

        # Backward tree:
        for i in range(self.n,0,-1):
            # Call
            self.t_eu_c[:i, i-1] = np.exp(-self.param.rate * self.dt) \
                * (self.p * self.t_eu_c[:i, i] \
                + (1 - self.p) * self.t_eu_c[1:i+1, i])

            # Put
            self.t_eu_p[:i, i-1] = np.exp(-self.param.rate * self.dt) \
                * (self.p * self.t_eu_p[:i, i] \
                + (1 - self.p) * self.t_eu_p[1:i+1, i])


    def set_american(self):
        """
        Set American call and put option
        """
        self.set_tree()

        self.t_am_c = self.t_stock.copy()
        self.t_am_p = self.t_stock.copy()

        self.t_am_c[:,-1] = np.maximum(self.t_stock[:,-1] \
            - self.param.strike,0.0)

        self.t_am_p[:,-1] = np.maximum(self.param.strike \
            - self.t_stock[:,-1], 0.0)

        for i in range(self.n-1,-1,-1):

            # Call
            ex_c = self.t_stock[:,i] - self.param.strike
            wait_c = np.exp(-self.param.rate * self.dt) \
                * (self.p * self.t_am_c[:i+1, i+1] \
                + (1 - self.p) * self.t_am_c[1:i+2, i+1])

            self.t_am_c[:i+1,i] = np.maximum(ex_c[:i+1], wait_c[:i+1])

            # Put
            ex_p =  self.param.strike - self.t_stock[:,i]
            wait_p = np.exp(-self.param.rate * self.dt) \
                * (self.p * self.t_am_p[:i+1, i+1] \
                + (1 - self.p) * self.t_am_p[1:i+2, i+1])

            self.t_am_p[:i+1,i] = np.maximum(ex_p[:i+1], wait_p[:i+1])
