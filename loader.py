"""

@author: Enrico Pasquariello
@mail: enrico.pasquariello94@gmail.com   
"""

import os
import pandas as pd
from datetime import date, timedelta
import yfinance as yf

def excel(list_ISIN) -> pd.DataFrame:
    
    dict_excel = {}
    
    for ISIN in list_ISIN:
        df_stock = pd.read_excel(os.path.abspath(r'input'+'\Historical_prices.xlsx'),
                      sheet_name=ISIN)
        dict_excel[ISIN] = df_stock
        
    df_portfolio = dict_excel[min(dict_excel,
        key=lambda ISIN: dict_excel[ISIN].shape[0])]
    
    for ISIN in dict_excel.keys():
        dict_excel[ISIN].rename(columns={'Last Price':ISIN},
                                inplace=True)
    
    for df in dict_excel.values():
        df_portfolio = pd.merge(df_portfolio,
                                df,
                                on='Date',
                                how='left',
                                suffixes=['_tbd',''])
            
    df_portfolio.drop(columns=[min(dict_excel,
        key=lambda ISIN: dict_excel[ISIN].shape[0])+'_tbd'],
                                     inplace=True)
    df_portfolio.dropna(axis=0,
                        inplace=True)
    
    df_portfolio.set_index('Date',inplace=True)

    return df_portfolio

#------------------------------------------------------------------------------

def data(list_ticker) -> pd.DataFrame:
    
    today = date.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = date.today()-timedelta(days=360*10) # For the last 10 years
    start_date = start_date.strftime('%Y-%m-%d')
    
    dict_excel = {}
    
    for ticker in list_ticker:
        try:
            df_stock = yf.download(tickers=ticker,
                              start=start_date,
                              end=end_date)['Adj Close']
            dict_excel[ticker] = df_stock
        except Exception as E:
            print(E)
    
    # Delete df that have data lenght of less than 1 year
    for ticker in list(dict_excel.keys()):
        if len(dict_excel[ticker])<=252:
            del dict_excel[ticker]
    
    df_portfolio = pd.DataFrame(dict_excel[min(dict_excel,
        key=lambda ticker: dict_excel[ticker].shape[0])])
    
    for ticker in dict_excel.keys():
        dict_excel[ticker] = pd.DataFrame(dict_excel[ticker])
        dict_excel[ticker].rename(columns={'Adj Close':ticker},
                                inplace=True)
    
    for df in dict_excel.values():
        df_portfolio = pd.merge(df_portfolio,
                                df,
                                on='Date',
                                how='left')
            
    df_portfolio.drop(columns=['Adj Close'],
                      inplace=True)
    df_portfolio.dropna(axis=0,
                        inplace=True)
    
    return df_portfolio