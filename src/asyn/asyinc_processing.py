import pandas 
import asyncio
import yfinance as yf
###
import os
import pandas as pd 
import numpy as np
from math import sqrt
import collections



DATA_FOLDER_PATH = "../../Documents/works/Anduril_Partner/data/similarweb_data/raw_data/"
DATA_OUTPUT_FOLDER_PATH = "../../Documents/works/Anduril_Partner/data/similarweb_data/processed_data/"
RAW_DATA_FILE = "linitems_ticker.csv"
SUPPORT_DATA = "ticker_infomation.csv"

data_path = os.path.join(DATA_OUTPUT_FOLDER_PATH, RAW_DATA_FILE)
suppport_data_path = os.path.join(DATA_FOLDER_PATH, SUPPORT_DATA)

df = pd.read_csv(data_path).head(100)
sub = pd.read_csv(suppport_data_path)
df = df.set_index(["ticker","date"]).sort_index()
tickers = df.index.get_level_values(0).unique()
print(tickers)

async def get_line_item(ticker):
    line_items_df = pd.DataFrame()
    company = yf.Ticker(ticker)
    
    ## bal
    balance = company.quarterly_balance_sheet.T.sort_index()
    financials = company.quarterly_financials.T.sort_index()
    
    line_items_df['Total_Revenue'] = financials['Total Revenue']
    line_items_df['Net_Income'] = financials['Net Income']
    line_items_df['Operating_Expenses'] = financials['Total Operating Expenses']
    line_items_df['Total_Assets'] = balance['Total Assets']
    line_items_df['Total_Liab'] = balance['Total Liab']
    line_items_df['Retained_Earnings'] = balance['Retained Earnings']
    
    line_items_df['Total_Revenue'] = line_items_df['Total_Revenue'].astype(float)
    line_items_df['Net_Income'] = line_items_df['Net_Income'].astype(float)
    line_items_df['Operating_Expenses'] = line_items_df['Operating_Expenses'].astype(float)
    
    return line_items_df

async def get_similar_features(ticker,df):
    similarweb_cols = ["Visit","Bounce_Rate","Visit_Duration","Visitor_desktop","Visitor_Mobile","Page/Visit"]
    tmp = df.loc[ticker][similarweb_cols]["2020":"2020"]
    tmp.index = pd.to_datetime(tmp.index)
    return tmp.groupby(by = [tmp.index.month, tmp.index.year]).mean()


async def get_Data(ticker):

    a = await get_line_item(ticker)
    b = await get_similar_features(ticker)

    ticker_result = []
    for line_item in a.columns:
        tmpb = b.copy()
        tmpb[line_item] = np.repeat(a[line_item].values,3)
        ticker_result.append(tmpb.corr()[[line_item]])

    ticker_result_df = pd.concat(ticker_result,axis = 1).iloc[:b.shape[1],:]
    ticker_result_df['ticker'] = ticker


    print(ticker)
    return ticker_result_df

async def main(): # coroutine
    # await sleeper(1, i=0)
    tasks = []
    for i, ticker in enumerate(tickers):
        tasks.append(
            asyncio.create_task(
                get_Data(ticker)
            )
        )

    results = await asyncio.gather(*tasks)
    
    print(results)

asyncio.run(main()) 