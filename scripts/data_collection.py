import sched, time
import json
import requests
import psycopg2
from dotenv import load_dotenv
import os
import schedule
from datetime import datetime
import yfinance as yf

class APIFailureException(Exception):
    pass


def get_data(company_list):
    data = {}
    for c in company_list:
        info = yf.Ticker(c).info
        # print(c)
        # print(info['ask'])
        # print(info['volume'])
        data[c] = (info['ask'], info['volume'])
    print(data)
    return data



def write_to_db(data): 
    """
    Example output json
    {'Meta Data': {'1. Information': 'Batch Stock Market Quotes', '2. Notes': 'IEX Real-Time', '3. Time Zone': 'US/Eastern'}, 'Stock Quotes': [{'1. symbol': 'GOOG', '2. pr
    ice': '1297.7600', '3. volume': '849580', '4. timestamp': '2019-11-13 16:51:00'}, {'1. symbol': 'AAP', '2. price': '158.6000', '3. volume': '1359961', '4. timestamp': 
    '2019-11-13 16:02:00'}]}
    """

    # add to DB bois
    # open the door to the glorious DB
    conn_string = "host="+ os.getenv("PG_HOST") + " port=" + os.getenv("PG_PORT") + " dbname=" + os.getenv("PG_DB") + " user=" + os.getenv("PG_USER") + " password="+ os.getenv("PG_PASS")
    conn = psycopg2.connect(conn_string)
    print("Connected!")
    #this needs to be updated with the new api 
    for key, value in data.items():
        #value = { price, volume }
        price = value[0]
        volume = value[1]
        print(key, price)
        query = """INSERT INTO stocks (ticker, timestamp, price, volume) VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\')""".format(key, datetime.now(), price, volume)
        #send to DB through the aforementioned opened door
        conn.cursor().execute(query)
        conn.commit()

def handler():
    try:
        #load_dotenv()
        companies = ['AAPL', 'GOOG', 'MSFT']
        data = get_data(companies)
        write_to_db(data)
    except Exception as e:
        # return {
        # 'statusCode': 500,
        # 'body': json.dumps('Something went wrong :()')
        # }
        print(e)
       
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
#weekayday() in range ()1, 6):   



if __name__ == "__main__":
    load_dotenv()
    schedule.every().hour.do(handler)
