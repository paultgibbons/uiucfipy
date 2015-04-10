import requests
import numpy as np
from yahoo import yahoo_url, historical_url
from stock import Stock
from datetime import date, timedelta


limit = 10

def get_info(symbols, time=30, max_iterations=5):
    '''
    Takes a list of symbols as input and outputs an array of
    stock objects. Stock information goes back time days. Since
    Yahoo API is not always reliable, allow up to max_iterations
    calls to the API
    '''
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

    return stocks[:10]

def get_correlation_matrix(stocks):
    prices = [s.recent_close_prices for s in stocks]
    return np.corrcoef(prices).round(4)