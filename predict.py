from yahoo import key_info_url, top_symbols
import numpy as np
import urllib2
import csv


def request_csv(url):
    '''
    Makes web call and returns csv file
    '''
    data = []
    response = urllib2.urlopen(url)
    if response.getcode() >= 500:
        raise Exception('Error on yahoo server', response.msg)
    if response.getcode() >= 400:
        raise Exception('Error in call formatting', response.msg)
    response_string = response.read()

    reader = csv.reader(response_string.split('\n'), delimiter=',')
    for row in reader:
        data.append(row)
    return data


def process(data):
    '''
    processes the data to remove n/a's, etc
    row 0 = symbol
    row 1 = earnings per share
    row 2 = predict next quarter EPS
    row 3 = dividend/share
    row 4 = book value
    row 5 = market capitalization
    row 6 = ebitda
    row 7 = price to sales
    row 8 = price to book
    row 9 = short ratio
    row 10 = percent change from 50 day average
    '''
    data.pop()
    numeric = []
    for row in data:
        for i in xrange(len(row)):
            if row[i].find('N') != -1:
                row[i] = '0.0'
        if row[5][:-1] == 'B':
            r5 = float(row[5][:-1])*1000
        else:
            r5 = float(row[5][:-1])
        if row[6][:-1] == 'B':
            r6 = float(row[6][:-1])*1000
        else:
            r6 = float(row[6][:-1])
        numeric.append([float(row[1]),
                        float(row[2]),
                        float(row[3]),
                        float(row[4]),
                        r5,
                        r6,
                        float(row[7]),
                        float(row[8]),
                        float(row[9]),
                        float(row[10][:-1])
                        ])
    return np.array(numeric)


def get_weights():
    '''
    Uses least squares with the top stocks to predict recent close prices
    '''
    top_url = key_info_url(top_symbols())
    data = request_csv(top_url)
    numeric_data = process(data)
    A = numeric_data[:, :9]
    b = numeric_data[:, 9]
    weights = np.linalg.lstsq(A, b)[0]
    return weights


def predict_change(symbol):
    '''
    Takes a single stock and predicts its change from 50 day average
    returns both guess and actual change
    '''
    weights = get_weights()
    symbol_url = key_info_url(symbol).replace('+', '')
    data = request_csv(symbol_url)
    numeric_data = process(data)
    guess = weights.dot(numeric_data[0, :9])
    actual = numeric_data[0, 9]
    return [guess, actual]
