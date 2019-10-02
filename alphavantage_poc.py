import json
import requests


def get_current_data(company_string):
    API_KEY = "SORWOB9VR89V9RRW"

    get_request = "https://www.alphavantage.co/query?" \
                  "function=BATCH_STOCK_QUOTES&apikey={0}&symbols={1}"

    response = requests.get(get_request.format(API_KEY, company_string))

    print(response)

if __name__ == '__main__':

