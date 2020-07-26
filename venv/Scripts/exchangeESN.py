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

if __name__ == '__main__':
    id = 'binance'
    symbol = 'BTC/USDT'
    lenData = 10000
    records = select_postgreSQL_ticker(lenData)
    dataplot(records)