# BinomialTree

This repository uses Binomial tree to price several types of derivative. 

------------------

How to use:

  option_param.py 
  
      Object that store parameters (stock , strike, etc...)
  
  crr.py:
  
      Class: BinomialTree
      Use Cox, Ross, and Rubinstein (1979) to price: 
      - European Call and Put
      - American Call and Put
  
  binomial_plot.py
  
      Object that plot Binomial Tree using two methodology. 
      - first method keeps tree branch proportional to price / rate etc..
      - second method is more aesthetic and keep tree branch distances
      equal. (up move = down move)
  
  
  Check notebook CRR_implementation.ipynb for full example using the 3 modules mentionned above

--------------------------

  short_interest_rate.py
  
    - Ho-Lee model (HoLee Class)
    - Black-Derman-Toy model (BlackDermanToy Class)
  
    Option IR  
    
      - Caps (~EU CALL)
      - Floors (~EU PUTS)
      - Swap
      - Swaption

  Check notebook Short_interest_rate.ipynb for full example
