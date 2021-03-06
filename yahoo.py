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


def key_info_url(symbols):
    '''
    returns key information for a list of symbols
    '''
    url = 'http://finance.yahoo.com/d/quotes.csv?s='
    url += '+'.join(symbols)+'&f=see9db4j1j4p5p6s7m8'
    return url


def top_symbols():
    '''
    gets list of 500 top stock symbols
    from wikipedia list
    '''
    return ['MMM',
            'ABT',
            'ABBV',
            'ACN',
            'ACE',
            'ACT',
            'ADBE',
            'ADT',
            'AES',
            'AET',
            'AFL',
            'AMG',
            'A',
            'GAS',
            'APD',
            'ARG',
            'AKAM',
            'AA',
            'ALXN',
            'ATI',
            'ALLE',
            'ADS',
            'ALL',
            'ALTR',
            'MO',
            'AMZN',
            'AEE',
            'AAL',
            'AEP',
            'AXP',
            'AIG',
            'AMT',
            'AMP',
            'ABC',
            'AME',
            'AMGN',
            'APH',
            'APC',
            'ADI',
            'AON',
            'APA',
            'AIV',
            'AAPL',
            'AMAT',
            'ADM',
            'AIZ',
            'T',
            'ADSK',
            'ADP',
            'AN',
            'AZO',
            'AVGO',
            'AVB',
            'AVY',
            'BHI',
            'BLL',
            'BAC',
            'BK',
            'BCR',
            'BAX',
            'BBT',
            'BDX',
            'BBBY',
            'BRK',
            'BBY',
            'BIIB',
            'BLK',
            'HRB',
            'BA',
            'BWA',
            'BXP',
            'BSX',
            'BMY',
            'BRCM',
            'BF',
            'CHRW',
            'CA',
            'CVC',
            'COG',
            'CAM',
            'CPB',
            'COF',
            'CAH',
            'HSIC',
            'KMX',
            'CCL',
            'CAT',
            'CBG',
            'CBS',
            'CELG',
            'CNP',
            'CTL',
            'CERN',
            'CF',
            'SCHW',
            'CHK',
            'CVX',
            'CMG',
            'CB',
            'CI',
            'XEC',
            'CINF',
            'CTAS',
            'CSCO',
            'C',
            'CTXS',
            'CLX',
            'CME',
            'CMS',
            'COH',
            'KO',
            'CCE',
            'CTSH',
            'CL',
            'CMCSA',
            'CMA',
            'CSC',
            'CAG',
            'COP',
            'CNX',
            'ED',
            'STZ',
            'GLW',
            'COST',
            'CCI',
            'CSX',
            'CMI',
            'CVS',
            'DHI',
            'DHR',
            'DRI',
            'DVA',
            'DE',
            'DLPH',
            'DAL',
            'XRAY',
            'DVN',
            'DO',
            'DTV',
            'DFS',
            'DISCA',
            'DISCK',
            'DG',
            'DLTR',
            'D',
            'DOV',
            'DOW',
            'DPS',
            'DTE',
            'DD',
            'DUK',
            'DNB',
            'ETFC',
            'EMN',
            'ETN',
            'EBAY',
            'ECL',
            'EIX',
            'EW',
            'EA',
            'EMC',
            'EMR',
            'ENDP',
            'ESV',
            'ETR',
            'EOG',
            'EQT',
            'EFX',
            'EQIX',
            'EQR',
            'Essex',
            'EL',
            'ES',
            'EXC',
            'EXPE',
            'EXPD',
            'ESRX',
            'XOM',
            'FFIV',
            'FB',
            'FDO',
            'FAST',
            'FDX',
            'FIS',
            'FITB',
            'FSLR',
            'FE',
            'FISV',
            'FLIR',
            'FLS',
            'FLR',
            'FMC',
            'FTI',
            'F',
            'FOSL',
            'BEN',
            'FCX',
            'FTR',
            'GME',
            'GCI',
            'GPS',
            'GRMN',
            'GD',
            'GE',
            'GGP',
            'GIS',
            'GM',
            'GPC',
            'GNW',
            'GILD',
            'GS',
            'GT',
            'GOOGL',
            'GOOG',
            'GWW',
            'HAL',
            'HBI',
            'HOG',
            'HAR',
            'HRS',
            'HIG',
            'HAS',
            'HCA',
            'HCP',
            'Health',
            'HP',
            'HES',
            'HPQ',
            'HD',
            'HON',
            'HRL',
            'HSP',
            'HST',
            'HCBK',
            'HUM',
            'HBAN',
            'ITW',
            'IR',
            'TEG',
            'INTC',
            'ICE',
            'IBM',
            'IP',
            'IPG',
            'IFF',
            'INTU',
            'ISRG',
            'IVZ',
            'IRM',
            'JEC',
            'JNJ',
            'JCI',
            'JOY',
            'JPM',
            'JNPR',
            'KSU',
            'K',
            'KEY',
            'GMCR',
            'KMB',
            'KIM',
            'KMI',
            'KLAC',
            'KSS',
            'KRFT',
            'KR',
            'LB',
            'LLL',
            'LH',
            'LRCX',
            'LM',
            'LEG',
            'LEN',
            'LVLT',
            'LUK',
            'LLY',
            'LNC',
            'LLTC',
            'LMT',
            'L',
            'LO',
            'LOW',
            'LYB',
            'MTB',
            'MAC',
            'M',
            'MNK',
            'MRO',
            'MPC',
            'MAR',
            'MMC',
            'MLM',
            'MAS',
            'MA',
            'MAT',
            'MKC',
            'MCD',
            'MHFI',
            'MCK',
            'MJN',
            'MWV',
            'MDT',
            'MRK',
            'MET',
            'KORS',
            'MCHP',
            'MU',
            'MSFT',
            'MHK',
            'TAP',
            'MDLZ',
            'MON',
            'MNST',
            'MCO',
            'MS',
            'MOS',
            'MSI',
            'MUR',
            'MYL',
            'NDAQ',
            'NOV',
            'NAVI',
            'NTAP',
            'NFLX',
            'NWL',
            'NFX',
            'NEM',
            'NWSA',
            'NEE',
            'NLSN',
            'NKE',
            'NI',
            'NE',
            'NBL',
            'JWN',
            'NSC',
            'NTRS',
            'NOC',
            'NRG',
            'NUE',
            'NVDA',
            'ORLY',
            'OXY',
            'OMC',
            'OKE',
            'ORCL',
            'OI',
            'PCAR',
            'PLL',
            'PH',
            'PDCO',
            'PAYX',
            'PNR',
            'PBCT',
            'POM',
            'PEP',
            'PKI',
            'PRGO',
            'PFE',
            'PCG',
            'PM',
            'PSX',
            'PNW',
            'PXD',
            'PBI',
            'PCL',
            'PNC',
            'RL',
            'PPG',
            'PPL',
            'PX',
            'PCP',
            'PCLN',
            'PFG',
            'PG',
            'PGR',
            'PLD',
            'PRU',
            'PEG',
            'PSA',
            'PHM',
            'PVH',
            'QEP',
            'PWR',
            'QCOM',
            'DGX',
            'RRC',
            'RTN',
            'O',
            'RHT',
            'REGN',
            'RF',
            'RSG',
            'RAI',
            'RHI',
            'ROK',
            'COL',
            'ROP',
            'ROST',
            'RCL',
            'R',
            'CRM']
