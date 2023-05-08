"""
This code creates the Markowitz efficient frontier for a list of given ISINs
(data source BBG) or tickers (data source Yahoo Finance)
and gives the optimal weights as output in order to maximize (or minimize)
the Sharpe Ratio (or negative Sharpe Ratio, SR)

@author: Enrico Pasquariello
@mail: enrico.pasquariello94@gmail.com
"""

from functions import loader, creator, saver

def main() -> None:
    
    # Load the data: src and ISIN/ticker to be set
    
    src = 'YAHOO'
    #src = 'BBG'
    
    list_ISIN = ['IT0005519787','IT0003256820','DE000A1E0HR8',]
    list_ticker = ['SPY','ACWI','SPTL',]
    
    if src == 'BBG':
        df_portfolio = loader.excel(list_ISIN)
    else:
        df_portfolio = loader.data(list_ticker)
    
    df_weights, df_corr = creator.efficient_frontier(df_portfolio,src)
    
    saver.excel(df_weights,df_corr)

#  ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()