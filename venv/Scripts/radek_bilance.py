# https://medium.com/ccxt/playing-with-ccxt-in-google-colab-23522ac8a6cb

import ccxt
binance = ccxt.binance () # Loads Binance
binance.load_markets ()
print ('binance: %d markets loaded!' % len (binance.markets))


# import warnings filter
from warnings import simplefilter
# ignore all future warnings (ignoruje pracovní varovné správy)
simplefilter(action='ignore', category=FutureWarning)


import matplotlib.pyplot as plt
#import matplotlib
# %config InlineBackend.figure_format = 'retina'
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')

plt.style.use ('seaborn-white')
plt.rcParams["figure.figsize"] = [15,6]

import pandas as pd
from datetime import datetime

pair = 'BTC/USDT'

# Load OHLCV (open/high/low/close/volume) data with 1-day resolution
ohlcv = binance.fetch_ohlcv(pair, '1d')

# Get closing prices for each day
prices = [x[4] for x in ohlcv]

# Convert Unix timestamps to Python dates
dates = [datetime.utcfromtimestamp(x[0] // 1000) for x in ohlcv]
# print('dates: ', dates)

# Prepare a Pandas series object
data = pd.Series (prices, index=dates)

# Draw a sipmle line chart
plt.plot(data)
plt.show()
