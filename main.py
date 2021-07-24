'''
Author: Gunnar Bowman
Date: 07/23/2021
Script to calculate the annual Sharpe Ratio of the S&P500
Uses the 1 year Treasury constant maturity rate as risk-free return.
'''

from fredapi import Fred
import numpy as npy
import datetime


def risk_free_rate(fred):
    # 1 year treasury constant maturity rate (sourced from Fred)
    riskfree = fred.get_series('DGS1')
    riskfree = riskfree[-1]
    return riskfree


def get_spy_series(fred):
    currentday = datetime.datetime.today()
    currentday = currentday.strftime('%m/%d/%Y')
    currentday = currentday[0:6] + str(int(currentday[7:10]) - 1)
    spy = fred.get_series('SP500', observation_start=currentday)
    spy = spy.dropna()
    return spy


def sharpe_ratio(riskfree, spy):
    dailyreturns = []
    for i in range(1, len(spy)):
        dailyreturns.append((spy[i] - spy[i-1])/spy[i-1])
    avg_daily_returns = sum(dailyreturns)/len(dailyreturns)
    std_daily_returns = npy.std(dailyreturns)
    sharperatio = ((avg_daily_returns - (riskfree/100)) /
                   std_daily_returns)*(len(spy) ** (1/2))
    return sharperatio


def main():
    fred = Fred(api_key='')
    riskfree = risk_free_rate(fred)
    spy = get_spy_series(fred)
    sharperatio = sharpe_ratio(riskfree, spy)
    print(sharperatio)


if __name__ == '__main__':
    main()
