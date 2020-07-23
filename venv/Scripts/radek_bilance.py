# -*- coding: utf-8 -*-
# https://medium.com/ccxt/playing-with-ccxt-in-google-colab-23522ac8a6cb

import os
import sys
import time

# -----------------------------------------------------------------------------

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

# -----------------------------------------------------------------------------


import ccxt

# -----------------------------------------------------------------------------
# common constants

msec = 1000
minute = 60 * msec
hold = 30

# -----------------------------------------------------------------------------

# binance
# bitfinex
exchange = ccxt.binance({
    'rateLimit': 10000,
    'enableRateLimit': True,
    # 'verbose': True,
})

# -----------------------------------------------------------------------------

# from_datetime = '2017-01-01 00:00:00'
from_datetime = '2020-07-22 00:00:00'
from_timestamp = exchange.parse8601(from_datetime)

# -----------------------------------------------------------------------------


exchange.load_markets ()
print ('exchange: %d markets loaded!' % len (exchange.markets))


# import warnings filter
from warnings import simplefilter
# ignore all future warnings (ignoruje pracovní varovné správy)
simplefilter(action='ignore', category=FutureWarning)


import matplotlib.pyplot as plt
# %config InlineBackend.figure_format = 'retina'
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')

plt.style.use ('seaborn-white')
plt.rcParams["figure.figsize"] = [15,6]

import pandas as pd
from datetime import datetime

pair = 'BTC/USDT'

# Load OHLCV (open/high/low/close/volume) data with 1-day resolution
ohlcv = exchange.fetch_ohlcv(pair, '5m', from_timestamp)
print("ohlcv: ", ohlcv)

# Get closing prices for each day
prices = [x[4] for x in ohlcv]
print("prices: ", prices)

# Convert Unix timestamps to Python dates
# dates = [datetime.utcfromtimestamp(x[0] // 1000) for x in ohlcv] # mezinárodní čas
dates = [datetime.fromtimestamp(x[0] // 1000) for x in ohlcv] # místní čas
print('dates: ', dates)

# Prepare a Pandas series object
data = pd.Series (prices, index=dates)

# Draw a sipmle line chart
plt.plot(data)
plt.show()
