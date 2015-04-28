import json
import numpy as np
from yahoo import yahoo_url, historical_url
from stock import Stock
from datetime import date, timedelta
import threading


lock = threading.Lock()


def request_json(url, gae=True):
    '''
    Abstraction of making the call to the url
    '''
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


def create_stock(quote, max_iterations, start, end, stocks, index):
    '''
    Create a stock from a quote
    '''
    if (quote['StockExchange'] == None):
        return
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
    stock = Stock(quote, close_prices)
    stock.index = index
    lock.acquire()
    stocks.append(stock)
    lock.release()


def parallel_stocks(quotes, time, max_iterations):
    '''
    Calculate the stock information in parallel
    The way it is currently implemented, it does not keep stocks in order
    of how they are called
    '''
    stocks = []
    start_date = date.today() - timedelta(time)
    start = start_date.strftime("%Y-%m-%d")
    end = date.today().strftime("%Y-%m-%d")
    threads = []
    i = 0
    for quote in quotes:
        i += 1
        args = [quote, max_iterations, start, end, stocks, i]
        thread = threading.Thread(target=create_stock, args=args)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    stocks.sort(key=lambda s: s.index)
    return stocks


def get_info(symbols, time=30, max_iterations=5):
    '''
    Takes a list of symbols as input and outputs an array of
    stock objects. Stock information goes back time days. Since
    Yahoo API is not always reliable, allow up to max_iterations
    calls to the API
    '''
    if len(symbols) == 0:
        return []
    symbols = symbols[:30]

    url = yahoo_url(symbols)
    data = request_json(url)

    if 'error' in data:
        raise Exception('Error in call to yahoo', data['error']['description'])
    quotes = data['query']['results']['quote']
    if (type(quotes) != list):
        quotes = [quotes]
    stocks = parallel_stocks(quotes, time, max_iterations)

    return stocks


def get_correlation_matrix(input):
    stocks = input
    if type(stocks[0]) == str:
        stocks = get_info(stocks)
    prices = [s.recent_close_prices*1.0 for s in stocks]
    return np.corrcoef(prices).round(4)
