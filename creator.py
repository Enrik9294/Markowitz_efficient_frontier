"""

@author: Enrico Pasquariello
@mail: enrico.pasquariello94@gmail.com   
"""

import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from functions import utilities


def efficient_frontier(df_portfolio, src) -> tuple([pd.DataFrame,
                                                    pd.DataFrame]):
    if src == 'BBG':
        df_returns = np.log(df_portfolio / df_portfolio.shift(-1))
    else:
        df_returns = np.log(df_portfolio / df_portfolio.shift(1))

    df_returns.dropna(axis=0,
                      inplace=True)

    # %% Create the frontier

    n_portfolios = 10_000
    weight = np.zeros((n_portfolios, len(df_portfolio.columns)))
    expected_return = np.zeros((n_portfolios, len(df_portfolio.columns)))
    expected_vol = np.zeros((n_portfolios, len(df_portfolio.columns)))
    sharpe_ratio = np.zeros((n_portfolios, len(df_portfolio.columns)))

    mean_returns = df_returns.mean() * 252

    # Compute the volatility using the corr matrix
    df_corr = df_returns.corr()
    st_dev = df_returns.std() * (252 ** 0.5)
    df_sigma = np.zeros_like(df_corr)
    np.fill_diagonal(df_sigma, st_dev ** 2)
    df_sigma = df_corr * np.outer(st_dev, st_dev)

    for n in range(n_portfolios):
        # Generate a random weight vector
        w = np.array(np.random.random(len(df_portfolio.columns)))
        w = w / np.sum(w)
        weight[n, :] = w

        # Expected return
        expected_return[n] = np.sum(mean_returns * w)

        # Expected volatility
        expected_vol[n] = (np.dot(w.T, np.dot(df_sigma, w)) ** 0.5)

        # Sharpe Ratio
        sharpe_ratio[n] = expected_return[n] / expected_vol[n]

    # Sharpe Ratio maximization

    max_sr_index = sharpe_ratio.argmax(axis=0)

    # %% Plot the frontier

    plt.figure()
    plt.scatter(expected_vol,
                expected_return,
                c=sharpe_ratio)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Returns')
    plt.title('Frontier')
    plt.colorbar(label='SR')
    plt.scatter(expected_vol[max_sr_index],
                expected_return[max_sr_index],
                c='r')

    # %% Get the optimal weights setting a min problem

    def negative_SR(w):
        w = np.array(w)
        R = np.sum(mean_returns * w)
        V = np.dot(w.T, np.dot(df_sigma, w)) ** 0.5
        sr = R / V
        return -1 * sr

    w0 = 1 / len(df_portfolio.columns)
    list_w0 = [w0] * len(df_portfolio.columns)
    bounds = ((0, 1),) * len(df_portfolio.columns)
    constraints = ({'type': 'eq',
                    'fun': utilities.check_sum_to_one})

    w_opt = minimize(negative_SR,
                     list_w0,
                     method='SLSQP',
                     bounds=bounds,
                     constraints=constraints)

    # %% Get the minimum volatility

    returns = np.linspace(-0.3, 0.3, 50)
    vol_opt = []

    def min_vol(w):
        w = np.array(w)
        V = np.dot(w.T, np.dot(df_sigma, w)) ** 0.5
        return V

    def get_return(w):
        w = np.array(w)
        R = np.sum(mean_returns * w)
        return R

    for r in returns:
        # Get the best volatility
        constraints = ({'type': 'eq',
                        'fun': utilities.check_sum_to_one},
                       {'type': 'eq',
                        'fun': lambda w: get_return(w) \
                                         - r})
        opt = minimize(min_vol,
                       list_w0,
                       method='SLSQP',
                       bounds=bounds,
                       constraints=constraints)
        vol_opt.append(opt['fun'])

    # %% Plot the Markowitz efficient frontier

    plt.figure()
    plt.scatter(expected_vol,
                expected_return,
                c=sharpe_ratio)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Returns')
    plt.title('Markowitz efficient frontier')
    plt.colorbar(label='SR')
    plt.scatter(expected_vol[max_sr_index],
                expected_return[max_sr_index],
                c='r')
    plt.plot(vol_opt, returns, '--')
    plt.show()

    # Create a df with optimal weights

    df_weights = pd.DataFrame({'Stock': list(df_portfolio.columns),
                               'Opt_weights_argmax': weight[max_sr_index[0], :],
                               'Opt_weights_SLSQP': w_opt.x, })

    return df_weights, df_corr