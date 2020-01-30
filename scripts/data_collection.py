import sched, time
import json
import requests
import psycopg2
from dotenv import load_dotenv
import os
import schedule
import datetime

class APIFailureException(Exception):
    pass


def get_data(company_list):
   
    API_KEY = os.getenv("API_KEY")
    API_KEY2 = os.getenv("API_KEY2")
    last_used = API_KEY2
    responses = []
    for c in company_list:
        if(last_used == API_KEY):
            current_key = API_KEY2
        else:
            current_key = API_KEY

        get_request = "https://www.alphavantage.co/query?" \
                  "function=BATCH_STOCK_QUOTES&apikey={0}&symbol={1}"
        response = requests.get(get_request.format(current_key, c))

        last_used = current_key

        if response.status_code != 200:
            raise APIFailureException("Something went wrong")

         print(response.json())
         responses.append(response.json())
    return responses


def write_to_db(data): 
    """
    Example output json
    {'Meta Data': {'1. Information': 'Batch Stock Market Quotes', '2. Notes': 'IEX Real-Time', '3. Time Zone': 'US/Eastern'}, 'Stock Quotes': [{'1. symbol': 'GOOG', '2. pr
    ice': '1297.7600', '3. volume': '849580', '4. timestamp': '2019-11-13 16:51:00'}, {'1. symbol': 'AAP', '2. price': '158.6000', '3. volume': '1359961', '4. timestamp': 
    '2019-11-13 16:02:00'}]}
    """

    # add to DB bois
    conn_string = "host="+ os.getenv("PG_HOST") + " port=" + os.getenv("PG_PORT") + " dbname=" + os.getenv("PG_DB") + " user=" + os.getenv("PG_USER") + " password="+ os.getenv("PG_PASS")
    conn = psycopg2.connect(conn_string)
    print("Connected!")

    stocks = data['Stock Quotes']
    for stock in stocks: 
        ticker = stock['1. symbol']
        price = float(stock['2. price'])
        timestamp = stock['4. timestamp']
        query = """INSERT INTO stocks (ticker, price, timestamp) VALUES (\'{0}\', \'{1}\', \'{2}\')""".format(ticker, price, timestamp)
        conn.cursor().execute(query)
        conn.commit()

def handler():
    try:
        #load_dotenv()
        companies = []
        if datetime.datetime.now().isoweekday(1, 6):
            data = get_data(companies)
            write_to_db(data)
    except:
        return {
        'statusCode': 500,
        'body': json.dumps('Something went wrong :()')
        }
       
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
weekayday() in range ()1, 6):   



if __name__ == "__main__":
    load_dotenv()
    schedule.every().day.at("9:00").do(handler)
    if(t)
    while True:
        schedule.run_pending()
        time.sleep(1)