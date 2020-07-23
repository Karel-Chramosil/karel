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

        cur.execute("SELECT count(*) FROM ticker")  # počet řádků tabulky ticker
        result = cur.fetchone()
        max_row_tab = result[0]
        print("max_row_tab: ", max_row_tab)
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

    return


if __name__ == '__main__':
    id = 'binance'
    symbol = 'BTC/USDT'
    lenData = 10000
    select_postgreSQL_ticker(lenData)
