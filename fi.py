import requests
from yahoo import yahoo_url, historical_url
from stock import Stock
from datetime import date, timedelta


def get_info(symbols, time=14, max_iterations=5):
    url = yahoo_url(symbols)
    response = requests.get(url)
    if response.status_code == 400:
        raise Exception('Error in call formatting', response.content)
    data = response.json()
    if 'error' in data:
        raise Exception('Error in call to yahoo', data['error']['description'])
    quotes = data['query']['results']['quote']
    stocks = []
    for quote in quotes:
        if (quote['StockExchange'] != None):
            start_date = date.today() - timedelta(time)
            start = start_date.strftime("%Y-%m-%d")
            end = date.today().strftime("%Y-%m-%d")

            success = False
            for i in range(max_iterations):
                if not success:
                    url = historical_url(quote['symbol'], start, end)
                    response = requests.get(url)
                    data = response.json()

                    if 'error' in data and i == 2:
                        raise Exception('Error in call to historical api',
                                        response.content)
                    elif 'error' not in data:
                        success = True

            quotes = data['query']['results']['quote']
            close_prices = [float(q['Close']) for q in quotes]

            stocks.append(Stock(quote, close_prices))

    return stocks
