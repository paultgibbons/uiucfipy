from fi import get_info
from yahoo import yahoo_url, historical_url
from stock import Stock
import unittest


class FiPyTest(unittest.TestCase):
    '''
    Test class for FiPy
    '''
    def test_yahoo_symbols_url(self):
        '''
        Test to create url from a given list of stock symbols
        '''
        yahoo_test_url = (r'https://query.yahooapis.com/v1/public/yql?q='
                          r'select%20*%20from%20yahoo.finance.quote%20where'
                          r'%20symbol%20in'
                          r'%20(%22A%22%2C%22B%22%2C%22C%22)&format=json&di'
                          r'agnostics=true'
                          r'&env=store%3A%2F%2Fdatatables.org%2Falltableswit'
                          r'hkeys&callback=')
        produced = yahoo_url(['A', 'B', 'C'])
        self.assertEqual(yahoo_test_url, produced)

    def test_yahoo_historical_url(self):
        '''
        Test to create url to get historical prices of a single stock
        '''
        yahoo_test_url = (r'https://query.yahooapis.com/v1/public/yql?q=sele'
                          r'ct%20*%20from%20yahoo.finance.historicaldata%20w'
                          r'here%20symbol%20%3D%20%22YHOO%22%20and%20startDa'
                          r'te%20%3D%20%222009-09-11%22%20and%20endDate%20%3'
                          r'D%20%222010-03-07%22&format=json&diagnostics=tru'
                          r'e&env=store%3A%2F%2Fdatatables.org%2Falltableswi'
                          r'thkeys&callback=')
        produced = historical_url('YHOO', '2009-09-11', '2010-03-07')
        self.assertEqual(yahoo_test_url, produced)

    def test_blank_yahoo(self):
        '''
        Test Exception thrown when no stocks are provided
        '''
        self.assertRaises(Exception, yahoo_url, [])

    def test_stock(self):
        '''
        Test stock class
        '''
        data = {}

        symbol = 'SYM'
        amount1 = 100
        amount2 = 10
        exchange = 'NYSE'

        data['symbol'] = symbol
        data['AverageDailyVolume'] = amount1
        data['Change'] = amount2
        data['DaysLow'] = 1
        data['DaysHigh'] = 1
        data['YearLow'] = 1
        data['YearHigh'] = 1
        data['MarketCapitalization'] = 1
        data['LastTradePriceOnly'] = 1
        data['DaysRange'] = 1
        data['Name'] = 'STOCK'
        data['Symbol'] = 'SYM'
        data['Volume'] = 1
        data['StockExchange'] = exchange

        s = Stock(data, [])

        self.assertEqual(s.symbol, symbol)
        self.assertEqual(s.AverageDailyVolume, amount1)
        self.assertEqual(s.Change, amount2)
        self.assertEqual(s.StockExchange, exchange)

    def test_get_stocks(self):
        '''
        Test main call that gets info on stocks by their symbols
        '''
        symbols = ["YHOO", "AAPL", "fakeStock", "MSFT"]
        stocks = get_info(symbols)
        self.assertEqual(len(stocks), 3)
        self.assertEqual(stocks[0].StockExchange, 'NMS')
        self.assertEqual(stocks[2].Symbol, 'MSFT')
        cp = stocks[0].recent_close_prices
        # Assuming yahoo does become terrible or super successful...
        if len(cp) < 3 or cp[2] < 0.05 or cp[2] > 9999.5:
            self.fail('Wrong close prices')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
