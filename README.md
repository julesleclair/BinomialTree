# BinomialTree

  -CRR model - Cox, Ross, and Rubinstein (1979)
    - European Call and Put
    - American Call and Put
  Comment: Just finish rewritting the tree to make it more efficient 
          i.e. use vectorisation instead of double loop!


-Short Interest Rate model: 
  -Ho-Lee model (HoLee Class)
  -Black-Derman-Toy model (BlackDermanToy Class)
  
  - Option IR  
    -Caps (~EU CALL)
    -Floors (~EU PUTS)
    -Swap
    -Swaption
  
How to use:
  - Check notebook CRR_implementation.ipynb for full example
  - option_param.py 
      Object that store parameters (stock , strike, etc...)
  - crr.py
      Object that calculate the binomial price of European and
      American option (call / put) using the CRR implementation.
  - binomial_plot.py
      Object that plot Binomial Tree using two methodology. 
      - first method keeps tree branch proportional to price / rate etc..
      - second method is more aesthetic and keep tree branch distances
      equal. (up move = down move)
  - short_interest_rate.py
    - HoLee model
    - simple BlackDermanToy model 
    - Option_IR: 
      - Cap
      - Floor
      - Swap
      - Swaption (~European call)
