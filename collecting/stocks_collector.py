import yfinance as yf
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from common.costants import target_company


def update_stocks(arg):
    for company in target_company:
        fname = "data/historical_data/" + company['ticker'] + ".json"
        if arg == 'init':
            start_date = "2021-01-18"
            end_date = "2022-01-18"
            fname = "../" + fname
            mode = 'w'
        elif arg == 'update':
            end_date = (datetime.now() + relativedelta(days=1)).strftime('%Y-%m-%d')
            with open(fname, mode='r') as saved_stocks:
                df = pd.read_json(path_or_buf=saved_stocks, orient='records', lines=True)
            df['Date'] = pd.to_datetime(df['Date'])
            last_insert = df['Date'].max()
            start_date = (last_insert + relativedelta(days=1)).strftime('%Y-%m-%d')
            mode = 'a'

        stocks_df = download_stocks(company['ticker'], start_date, end_date)
        # stocks_df = stocks_df.drop_duplicates(subset=['Date'], keep='last')
        with open(fname, mode=mode, encoding='utf-8') as stocks_json:
            stocks_df.to_json(path_or_buf=stocks_json, orient='records', lines=True, index=True, date_format='iso')
    # SPY index
    fname = "data/historical_data/S&P500.json"
    if arg == 'init':
        fname = "../" + fname
    index_df = download_stocks('SPY', start_date, end_date)
    with open(fname, mode=mode, encoding='utf-8') as stocks_json:
        index_df.to_json(path_or_buf=stocks_json, orient='records', lines=True, index=True, date_format='iso')


def download_stocks(ticker, start_date, end_date):
    ticker = yf.Ticker(ticker)
    hist = ticker.history(start=start_date, end=end_date)
    hist.reset_index(inplace=True)
    return hist


# init the storage
if __name__ == "__main__":
    update_stocks('init')