class Stock:
    '''
    Class to represent a single stock
    '''
    def __init__(self, info, close_prices):
        self.symbol = info['symbol']
        self.AverageDailyVolume = info['AverageDailyVolume']
        self.Change = info['Change']
        self.DaysLow = info['DaysLow']
        self.DaysHigh = info['DaysHigh']
        self.YearLow = info['YearLow']
        self.YearHigh = info['YearHigh']
        self.MarketCapitalization = info['MarketCapitalization']
        self.LastTradePriceOnly = info['LastTradePriceOnly']
        self.DaysRange = info['DaysRange']
        self.Name = info['Name']
        self.Symbol = info['Symbol']
        self.Volume = info['Volume']
        self.StockExchange = info['StockExchange']

        self.recent_close_prices = close_prices

        # optionally annually
        period = 'quarterly'
        statements_url = 'https://finance.yahoo.com/q/%s?s=%s+%s&' + period

        self.is_url = statements_url % ('is', self.symbol, 'Income+Statement')
        self.bs_url = statements_url % ('bs', self.symbol, 'Balance+Sheet')
        self.cf_url = statements_url % ('cf', self.symbol, 'Cash+Flow')
