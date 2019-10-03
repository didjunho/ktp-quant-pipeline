import sched, time
import requests


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


if __name__ == '__main__':
    input = "AAPL,GOOG"

    while True:
        get_data(input)
        time.sleep(60)
