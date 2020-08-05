# -*- coding: utf-8 -*-

import os
import sys
import time
import psycopg2
from config import config

# -----------------------------------------------------------------------------

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

# -----------------------------------------------------------------------------

import ccxt  # noqa: E402

# -----------------------------------------------------------------------------


def read_ohlcv(symbol):

    try:
        # binance
        # bitfinex

        exchange = ccxt.binance({
            'rateLimit': 10000,
            'enableRateLimit': True,
            # 'verbose': True,
        })
        print("exchange: ", exchange)

        # from_datetime = '2017-01-01 00:00:00'
        from_datetime = '2020-08-04 00:00:00'
        from_timestamp = exchange.parse8601(from_datetime)
        #
        # print("from_timestamp: ", from_timestamp)

        msec = 1000
        minute = 60 * msec
        hour = minute * 60
        hold = 30

        # -----------------------------------------------------------------------------

        now = exchange.milliseconds()
        # print("now: ", now)

        # -----------------------------------------------------------------------------

        data = []

    except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
        print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
        time.sleep(hold)
    finally:
        print()
        # print('Datum pro ohlcv zadáno.')


    while from_timestamp < now:

        try:

            print(exchange.milliseconds(), 'Fetching candles starting from', exchange.iso8601(from_timestamp))
            ohlcvs = exchange.fetch_ohlcv(symbol, '1h', from_timestamp)
            print(exchange.milliseconds(), 'Fetched', len(ohlcvs), 'candles')
            if len(ohlcvs) > 0:
                first = ohlcvs[0][0]
                last = ohlcvs[-1][0]
                print('First candle epoch', first, exchange.iso8601(first))
                print('Last candle epoch', last, exchange.iso8601(last))
                # from_timestamp += len(ohlcvs) * minute * 5  # very bad
                from_timestamp = ohlcvs[-1][0] + hour  # good
                data += ohlcvs
                # print('Len data : ', len(data))
                # print('Data: #####', data, '######')
                insert_postgreSQL_ohlcv(data)
                data = []

        except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
            print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
            time.sleep(hold)
        finally:
            print('Data ohlcv načtena.')

    return

    # -----------------------------------------------------------------------------

def insert_postgreSQL_ohlcv(data):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        cur.execute("SELECT MAX(timestamp) FROM ohlcv")  # poslední datum záznamu
        result = cur.fetchone()
        timestamp_max = result[0]
        print("timestamp_max: ", timestamp_max)


        i = 0
        while i <= len(data):
            if data[i][0] > timestamp_max:
                data_ohlcv = (data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5])
                print(data_ohlcv)
                sql_ohlcv = ("INSERT INTO ohlcv (timestamp, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s) ;")
                cur.execute(sql_ohlcv, data_ohlcv)
                conn.commit()
            i = i + 1

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
           conn.close()
           print('Database connection closed.')

    return

    # -----------------------------------------------------------------------------

if __name__ == '__main__':
    # -----------------------------------------------------------------------------
    # common constants

    symbol = 'BTC/USDT'

    # -----------------------------------------------------------------------------
    read_ohlcv(symbol)


