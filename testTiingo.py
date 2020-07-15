import pandas as pd
from io import StringIO
from tiingo import TiingoClient
import pickle
import config

API_KEY = '' # your API KEY here
client = TiingoClient({'api_key': "2727ca12f68fce3c489fb8bec1ff67b04d90b307"})

df = pd.read_csv(StringIO(client.get_ticker_price('AAPL',
    fmt='csv',
    frequency='daily',
    startDate= '07-14-2020',
    endDate='12-30-2020')))

print(df)