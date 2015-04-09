def yahoo_url(symbols):
    '''
    Create url to get stock information from yahoo finance
    '''
    if len(symbols) == 0:
        raise Exception('Need at least one stock')

    protocol = r'https://'
    base = r'query.yahooapis.com'
    version = 'v1'
    access = 'public'

    url = protocol + base + '/' + version + '/' + access + '/'
    url += (r'yql?q=select%20*%20from%20yahoo.finance.quote%20where'
            r'%20symbol%20'+'in%20(')
    for symbol in symbols:
        url += r'%22' + symbol + r'%22%2C'

    # Remove extra %2C at the end
    url = url[:-3]

    url += (r')&format=json&diagnostics=true&env=store'
            r'%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=')

    return url


def historical_url(symbol, start_date, end_date):
    '''
    Create url to get info on single historical stock
    '''
    protocol = r'https://'
    base = r'query.yahooapis.com'
    version = 'v1'
    access = 'public'

    url = protocol + base + '/' + version + '/' + access + '/'
    url += (r'yql?q=select%20*%20from%20yahoo.finance.historical'
            r'data%20where%20symbol%20%3D%20%22')
    url += symbol
    url += r'%22%20and%20startDate%20%3D%20%22'
    url += start_date
    url += r'%22%20and%20endDate%20%3D%20%22'
    url += end_date

    url += (r'%22&format=json&diagnostics=true&env=store'
            r'%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=')

    return url
