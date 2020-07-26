# -*- coding: utf-8 -*-
"""
Created on 23-07-2020

@author: Chramosil

Načtení dat z databáze

Predikce ESN dat a uložení do databáze

Zobrazení dat

"""
import os
import sys
import psycopg2
from config import config


import matplotlib.pyplot as plt
# %config InlineBackend.figure_format = 'retina'
from IPython.display import set_matplotlib_formats

import pandas as pd
from datetime import datetime

import numpy as np
from pyESN import ESN

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

def select_postgreSQL_ticker(lenData):
    """ Connect to the PostgreSQL tab tisker and read Data (number: lenData) """
    conn = None
    try:
        # read connection parameters
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        cur.execute("SELECT count(*) FROM ohlcv")  # počet řádků tabulky ticker
        result = cur.fetchone()
        max_row_tab = result[0]
        print("max_row_tab: ", max_row_tab)

        cur.execute("SELECT timestamp, close FROM ohlcv ORDER BY timestamp ASC")
        records = cur.fetchall()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

    return records


def dataplot(records):
    print("Total rows are:  ", len(records))
    print("Printing each row")
    print("\n")
    prices = [row[1] for row in records]
    #print("prices: ", prices)
    # dates = [datetime.fromtimestamp(row[0] // 1000) for row in records]  # místní čas
    dates = [datetime.fromtimestamp(row[0] // 1000) for row in records]  # místní čas
    #print('dates: ', dates)

    # Prepare a Pandas series object
    data = pd.Series(prices, index=dates)
    print('data: ', data)

    set_matplotlib_formats('retina')

    plt.style.use('seaborn-white')
    plt.rcParams["figure.figsize"] = [15, 6]

    # Draw a sipmle line chart
    plt.plot(data)
    plt.show()

    return

def dataprediction(records):
    rng = np.random.RandomState(42)
    esn = ESN(n_inputs = 1,
              n_outputs = 1,
              n_reservoir = 1000,
              spectral_radius = 0.25,
              sparsity = 0.95,
              noise = 0.001,
              # input_shift = [0, 0],
              input_shift = [0],
              # input_scaling = [0.01, 3],
              # input_scaling = [0.01],
              teacher_scaling = 1.12,
              teacher_shift = -0.7,
              out_activation = np.tanh,
              inverse_out_activation = np.arctanh,
              random_state = rng,
              silent = False
              )

    prices = [float(row[1]) for row in records]
    print("prices: ", prices)
    max_price = max(prices)
    min_price = min(prices)
    print("max_price: ", max_price, "   min_price: ", min_price)
    norma_prices = []
    for x in prices:
        norma_prices.append(x/(max_price + min_price))
    print("norma_prices: ", norma_prices)
    # Prepare a Pandas series object
    data = np.array(norma_prices)
    print('data: ', data)

    trainlen = 25000
    future = 10
    pred_training = esn.fit(np.ones(trainlen), data[:trainlen])

    prediction = esn.predict(np.ones(future))
    print("test error: \n" + str(np.sqrt(np.mean((prediction.flatten() - data[trainlen:trainlen + future]) ** 2)) * 100), "%")

    plt.figure(figsize=(11, 1.5))
    plt.plot(range(0, trainlen + future), data[0:trainlen + future], 'k', label="target system")
    plt.plot(range(trainlen, trainlen + future), prediction, 'r', label="free running ESN")
    lo, hi = plt.ylim()
    plt.plot([trainlen, trainlen], [lo + np.spacing(1), hi - np.spacing(1)], 'k:')
    plt.legend(loc=(0.61, 1.1), fontsize='x-small')
    plt.show()

    return

if __name__ == '__main__':
    id = 'binance'
    symbol = 'BTC/USDT'
    lenData = 10000
    records = select_postgreSQL_ticker(lenData)
    # dataplot(records)
    dataprediction(records)