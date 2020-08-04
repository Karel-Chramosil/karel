# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 22:24:43 2017

@author: Radek Chramosil

Uložení dat do databáze cisla

"""
import asyncio
import os
import sys
import psycopg2
from config import config
import radek_asciichart
from termcolor import colored
# from datetime import *
# import datetime


root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt  # noqa: E402


# ************************************************************
# Database postgreSQL

def test_connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()

        # ***********************************
        # PostgreSQL výpis tabulky cislo

        cur1 = conn.cursor()

        # execute a statement
        print('PostgreSQL výpis tabulky crypt_exch:')
        cur1.execute('SELECT * FROM crypt_exch ')

        # display the PostgreSQL database server version
        row = cur1.fetchone()
        print(row)  # tisk první řádek

        while row is not None:
            # print(row)
            row = cur1.fetchone()

            # close the communication with the PostgreSQL
        cur1.close()

    # ************************************

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return


# ********************* konec pokus_connect ***********************

async def test(id, symbol):
    exchange = getattr(ccxt, id)({
        'enableRateLimit': True,  # required according to the Manual
    })
    ticker = await exchange.fetch_ticker(symbol)
    await exchange.close()
    return ticker


def insert_postgreSQL_info(ticker):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur1 = conn.cursor()

        data_ticker1 = (ticker['info']['askPrice'], ticker['info']['askQty'], ticker['info']['bidPrice'],
                        ticker['info']['bidQty'], ticker['info']['closeTime'], ticker['info']['count'],
                        ticker['info']['firstId'], ticker['info']['highPrice'], ticker['info']['lastId'],
                        ticker['info']['lastPrice'], ticker['info']['lastQty'], ticker['info']['lowPrice'],
                        ticker['info']['openPrice'], ticker['info']['openTime'], ticker['info']['prevClosePrice'],
                        ticker['info']['priceChange'], ticker['info']['priceChangePercent'],
                        ticker['info']['quoteVolume'],
                        ticker['info']['symbol'], ticker['info']['volume'], ticker['info']['weightedAvgPrice'])
        sql_ticker1 = (
            "INSERT INTO info (askPrice, askQty, bidPrice, bidQty, closeTime, count, firstId, highPrice, lastId, "
            "lastPrice, "
            "lastQty, lowPrice, openPrice, openTime, prevClosePrice, priceChange, priceChangePercent, quoteVolume, "
            "symbol, "
            "volume, weightedAvgPrice) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s) ;")
        # print('sql_ticker1 = ', sql_ticker1)
        cur1.execute(sql_ticker1, data_ticker1)
        conn.commit()
        cur1.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')

    return


def insert_postgreSQL_ticker(ticker):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        data_ticker = (ticker['ask'], ticker['askVolume'], ticker['average'], ticker['baseVolume'], ticker['bid'],
                       ticker['bidVolume'], ticker['change'], ticker['close'], ticker['datetime'], ticker['high'],
                       ticker['last'], ticker['low'], ticker['open'], ticker['percentage'], ticker['previousClose'],
                       ticker['quoteVolume'], ticker['symbol'], ticker['timestamp'], ticker['vwap'])
        sql_ticker = (
            "INSERT INTO ticker (ask, askVolume, average, baseVolume, bid, bidVolume, change, close, datetime, high, "
            "last, low, open, percentage, previousClose, quoteVolume, symbol, timestamp, vwap) VALUES (%s, %s, %s, "
            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ;")
        cur.execute(sql_ticker, data_ticker)
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')

    return


def read_tickers(id, symbol):
    run = True
    ticker_dic = asyncio.get_event_loop().run_until_complete(test(id, symbol))
    width = 60
    series_bid = [ticker_dic['bid'] + 1]
    series_ask = [ticker_dic['ask'] + 1]
    j = 0

    try:
        while run:
            ticker_dic = asyncio.get_event_loop().run_until_complete(test(id, symbol))
            # pprint(ticker_dic)
            insert_postgreSQL_ticker(ticker_dic)
            # insert_postgreSQL_info(ticker_dic)
            if j < width:
                j = j + 1
            else:
                series_bid.pop(0)
                series_ask.pop(0)
            series_bid.append(ticker_dic['bid'])
            series_ask.append(ticker_dic['bid'])
            print("\n")
            print(colored(radek_asciichart.pplot(series_bid, series_ask), 'yellow'))
            #print((radek_asciichart.pplot(series)))
            print(colored('bid => ₿ = $ ','yellow'), colored(ticker_dic['bid'], "yellow"),
                  colored('              ask => ₿ = $ ','red'), colored(ticker_dic['ask'],'red'))
            # print("\n")
    except Exception as e:
        print('Error: ', e)
    finally:
        print('Konec programu načítání dat')
    return


if __name__ == '__main__':
    id = 'binance'
    symbol = 'BTC/USDT'
    read_tickers(id, symbol)
