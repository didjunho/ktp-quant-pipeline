import sched, time
import requests
import sqlite3

class APIFailureException(Exception):
    pass


def get_data(company_string):
    # Jonah's API key
    api_key = "SORWOB9VR89V9RRW"

    get_request = "https://www.alphavantage.co/query?" \
                  "function=BATCH_STOCK_QUOTES&apikey={0}&symbols={1}"

    response = requests.get(get_request.format(api_key, company_string))

    if response.status_code != 200:
        raise APIFailureException("Something went wrong")

    print(response.json())





def query_db(db_file,query,args=(),one=False):
    conn = create_connection(db_file)
    curs = conn.cursor()
    curs.execute(query)
    r_v = curs.fetchall()
    conn.commit()
    conn.close
    return (r_v[0] if r_v else None) if one else r_v



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print("Something went wrong in creating DB connection")
        
    return conn









def main():
    #query = "INSERT INTO tickers(tickName) VALUES('JPMOR');"
    #print(query_db('./sql/myDatabase.sqlite3', query))
    query_db("./sql/myDatabase.sqlite3", "INSERT INTO tickers(tickName) VALUES('APPL')")
    print(query_db('./sql/myDatabase.sqlite3', "SELECT * FROM tickers"))
    # print(query_db('./sql/myDatabase.sqlite3', "DELETE FROM * FROM tickers"))

    """
    input = "AAPL,GOOG"

    while True:
        get_data(input)
        time.sleep(60)
    """


if __name__ == '__main__':
    main()