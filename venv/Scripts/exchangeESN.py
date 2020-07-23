# -*- coding: utf-8 -*-
"""
Created on 23-07-2020

@author: Chramosil

Načtení dat z databáze

Predikce ESN dat a uložení do databáze

Zobrazení dat

"""

import psycopg2
from config import config


def insert_postgreSQL_ticker(lenData)
    """ Connect to the PostgreSQL tab tisker and read Data (number: lenData) """
    conn = None
    try:
        # read connection parameters
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql_max_row_tab = ("SELECT count(*) FROM ticker;")
        result = cur.execute(sql_max_row_tab)
        max_row_tab = result[0]
        print("max_row_tab: ", max_row_tab)
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')

    return

