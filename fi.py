import json
import numpy as np
from yahoo import yahoo_url, historical_url
from stock import Stock
from datetime import date, timedelta


limit = 10

def request_json(url, gae=True):
    data = None
    try:
        from google.appengine.api import urlfetch
        urlfetch.set_default_fetch_deadline(30)
        response = urlfetch.fetch(url)
        if response.status_code >= 500:
            raise Exception('Error on yahoo server', response.msg)
        if response.status_code >= 400:
            raise Exception('Error in call formatting', response.msg)
        response_string = response.content
        data = json.loads(response_string)
    except:
        import urllib2
        response = urllib2.urlopen(url)
        if response.getcode() >= 500:
            raise Exception('Error on yahoo server', response.msg)
        if response.getcode() >= 400:
            raise Exception('Error in call formatting', response.msg)
        response_string = response.read()
        data = json.loads(response_string)
    return data

def get_info(symbols, time=30, max_iterations=5):
    '''
    Takes a list of symbols as input and outputs an array of
    stock objects. Stock information goes back time days. Since
    Yahoo API is not always reliable, allow up to max_iterations
    calls to the API
    '''
    if len(symbols) == 0:
        return []

    url = yahoo_url(symbols)
    data = request_json(url)

    if 'error' in data:
        raise Exception('Error in call to yahoo', data['error']['description'])
    quotes = data['query']['results']['quote']
    if (type(quotes) != list):
        quotes = [quotes]
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
                    data = request_json(url)

                    if 'error' in data and i == (max_iterations-1):
                        raise Exception('Error in call to historical api',
                                        data)
                    elif 'error' not in data:
                        success = True

            quotes = data['query']['results']['quote']
            close_prices = [float(q['Close']) for q in quotes]

            stocks.append(Stock(quote, close_prices))

    return stocks[:10]

def get_correlation_matrix(input):
    stocks = input
    if type(stocks[0]) == str:
        stocks = get_info(stocks)
    prices = [s.recent_close_prices for s in stocks]
    return np.corrcoef(prices).round(4)