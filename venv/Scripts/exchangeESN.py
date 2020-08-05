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

def select_postgreSQL_close():
    """ Connect to the PostgreSQL tab ohlcv and read Data  """
    conn = None
    try:
        # read connection parameters
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # cur.execute("SELECT count(*) FROM ohlcv")  # počet řádků tabulky ticker
        # result = cur.fetchone()
        # max_row_tab = result[0]
        # print("max_row_tab: ", max_row_tab)

        cur.execute("SELECT timestamp, close, future FROM ohlcv ORDER BY timestamp ASC")
        records = cur.fetchall()
        cur.close()
        # print("records: ", records)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

    return records

def update_db_future(records, trlen, prediction, future):
    """ Connect to the PostgreSQL database server and update to tab ohlcv column future """
    conn = None
    try:
        # read connection parameters
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
        trlen = trlen - 1
        i = 1
        while i <= future // 2:
            predic = prediction[i] * (max_price + min_price)
            timestamp = int(records[(trlen + i)][0])
            parama = tuple(predic)
            paramb = parama + (timestamp,)  # Tuple
            print("i: ", i, " trlen + i: ", trlen + i + 1, " paramb: ", paramb)
            sql_ohlcv = ("UPDATE ohlcv SET future = %s WHERE timestamp = %s")
            cur.execute(sql_ohlcv, paramb)
            conn.commit()
            # print("param: ", paramb)
            i = i + 1

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')


    return

def dataplot(records):
    print("Total rows are:  ", len(records))
    print("Printing each row")
    print("\n")
    print("records: ", records)


    prices = [row[1] for row in records]
    volume = [row[2] for row in records]
    #print("prices: ", prices)
    # dates = [datetime.fromtimestamp(row[0] // 1000) for row in records]  # místní čas
    dates = [datetime.fromtimestamp(row[0] // 1000) for row in records]  # místní čas
    #print('dates: ', dates)

    # Prepare a Pandas series object
    dataprices = pd.Series(prices, index=dates)
    print('dataprices: ', dataprices)
    datavolume = pd.Series(volume, index=dates)
    print('datavolume: ', datavolume)

    set_matplotlib_formats('retina')

    plt.style.use('seaborn-white')
    plt.rcParams["figure.figsize"] = [15, 6]

    # Draw a sipmle line chart
    plt.plot(dataprices)
    plt.plot(datavolume)

    plt.show()

    return

def norma_prices(records):
    """ normuje data na rozsah <0,1> a převede data na np.array. """
    prices = [float(row[1]) for row in records]
    # print("prices: ", prices)
    max_price = max(prices)
    min_price = min(prices)
    print("max_price: ", max_price, "   min_price: ", min_price)
    norma_prices = []
    for x in prices:
        norma_prices.append(x/(max_price + min_price))
    # print("norma_prices: ", norma_prices)
    # Prepare a Pandas series object
    data = np.array(norma_prices)
    # print('data: ', data)
    return data, max_price, min_price

def dataprediction(data, max_price, min_price,future, show, inspect):


    trainlen = len(data) - future

    pred_training = esn.fit(np.ones(trainlen), data[:trainlen], inspect)

    prediction = esn.predict(np.ones(future))
    testerror = np.sqrt(np.mean((prediction.flatten() - data[trainlen:trainlen + future]) ** 2)) * 100

    if show:
        print("test error: \n" + str(testerror), "%")
        pred_training = pred_training * (max_price + min_price)
        # print("pred_training: ", pred_training)
        prediction = prediction * (max_price + min_price)
        # print("prediction", prediction)
        plt.figure(figsize=(11, 1.5))
        plt.plot(range(0, trainlen + future), data[0:trainlen + future] * (max_price + min_price), 'k', label="target system")
        plt.plot(range(trainlen, trainlen + future), prediction, 'r', label="free running ESN")
        lo, hi = plt.ylim()
        plt.plot([trainlen, trainlen], [lo + np.spacing(1), hi - np.spacing(1)], 'k:')
        plt.legend(loc=(0.61, 1.1), fontsize='x-small')
        plt.show()

    return

def futureprediction(records, data, fromrow, max_price, min_price, future):
    datalen = len(data)
    trainlen = fromrow - future

    while trainlen <= datalen:
        pred_training = esn.fit(np.ones(trainlen), data[:trainlen], inspect)
        prediction = esn.predict(np.ones(future))
        if trainlen <= datalen - future:
            testerror = np.sqrt(np.mean((prediction.flatten() - data[trainlen:trainlen + future]) ** 2)) * 100
            print("test error: " + str(testerror), "%", "trainlen: ", trainlen)
            trainlen = trainlen + (future // 2)
        else:
            if trainlen >= datalen - 1:
                return
            future = datalen - trainlen
            trainlen = datalen - future

        update_db_future(records, trainlen, prediction, future)

    return

if __name__ == '__main__':
    id = 'binance'
    symbol = 'BTC/USDT'

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
              silent = True
              )


    records = select_postgreSQL_close()
    dataplot(records)

    exit()

    # Předpověď dat
    data, max_price, min_price = norma_prices(records)
    future = 30 # na třicet dní, ukládám 15 dní
    inspect = False # optionally visualize the collected states
    plotshow = True # visualize prediction
    # dataprediction(data, max_price, min_price, future, plotshow, inspect)
    fromrow = len(data) - 160  # 1920 = 80 * 24 hod => 80 dní zpětně !!!!!!!!!!
    futureprediction(records, data, fromrow, max_price, min_price, future)
