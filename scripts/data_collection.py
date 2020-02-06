import sched, time
import json
import requests
import psycopg2
from dotenv import load_dotenv
import os
import schedule
from datetime import datetime
class APIFailureException(Exception):
    pass


def get_data(company_list):
   # for c inc 
    #API_KEY = os.getenv("API_KEY")
    API_KEY = "pk_4418eb83aa1444959a82a1303e9ce418"
    current = -1
    responses = []
    #for c in company_list:
        #current = (current + 1) % len(API_KEYS)

    get_request = "https://cloud.iexapis.com/v1/stock/market/batch/latestprice?symbols={0}&types=quote,chart&token={1}"
    response = requests.get(get_request.format(API_KEY, c))

    if response.status_code != 200:
        raise APIFailureException("Something went wrong")

    print(response.json())
    #responses.append(response.json())
    return response



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
        ticker = stock['symbol']
        price = float(stock['latestPrice '])
        timestamp = stock['latestUpdate']
        query = """INSERT INTO stocks (ticker, price, timestamp) VALUES (\'{0}\', \'{1}\', \'{2}\')""".format(ticker, price, timestamp)
        conn.cursor().execute(query)
        conn.commit()

def handler():
    try:
        #load_dotenv()
        companies = "aapl,goog,msft"
        #if datetime.datetime.now().isoweekday(1, 6):
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
#weekayday() in range ()1, 6):   



if __name__ == "__main__":
    load_dotenv()
    #schedule.every().day.at("9:00").do(handler)
    handler()
    
    #while True:
     #   now = datetime.now()
      #  current_time = now.strftime("%H:%M:%S")
       # if(current_time == "16:00:00"):
        #    schedule.cancel_job()
        #schedule.run_pending()
        #time.sleep(1)