import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from cleaning_data_functions import *


pc_dir = r'C:\Users\19059\Simple Python Projects\private-credit'
re_dir = r'C:\Users\19059\Simple Python Projects\private-reit-simulation'
hf_dir = r'C:\Users\19059\Simple Python Projects\hedge-fund-simulation'

private_credit = pd.read_csv(pc_dir + r'\composite private credit.csv')
reits = pd.read_csv(re_dir + r'\composite reit returns.csv')
hedge_funds = pd.read_csv(hf_dir + r'\composite hedge fund returns.csv')

# adjusting the private credit DataFrame
private_credit.rename({'Unnamed: 0': 'Date', '0': 'private_credit'}, axis=1, inplace=True)
private_credit['Date'] = pd.to_datetime(private_credit['Date'], dayfirst=False)
private_credit.set_index('Date', inplace=True)

# adjusting the reit DataFrame
reits.rename({'Unnamed: 0': 'Date', 'composite index': 'reits'}, axis=1, inplace=True)
reits['Date'] = pd.to_datetime(reits['Date'], dayfirst=False)
reits.set_index('Date', inplace=True)

# adjusting the hedge fund DataFrame
hedge_funds.rename({'Unnamed: 0': 'Date', 'composite': 'hedge funds'}, axis=1, inplace=True)
hedge_funds['Date'] = pd.to_datetime(hedge_funds['Date'], dayfirst=False)
hedge_funds.set_index('Date', inplace=True)

# adjusting the publicly traded DataFrame
spy_tlt_gld = pd.read_csv('spy_tlt_gld.csv')
spy_tlt_gld['Date'] = pd.to_datetime(spy_tlt_gld['Date'], dayfirst=False)
spy_tlt_gld.set_index('Date', inplace=True)
spy_tlt_gld = spy_tlt_gld.pct_change()

fund_list = [private_credit, reits, hedge_funds, spy_tlt_gld]

starting = [fund.index[0] for fund in fund_list]
ending = [fund.index[-1] for fund in fund_list]

start_date = start_date_finder(dates=starting, how='newest')
end_date = end_date_finder(dates=ending, how='oldest')

date_range = pd.date_range(start_date, end_date, freq='D')

alternatives = pd.DataFrame(index=date_range)


for fund in fund_list:

    x = 0

    for column in fund.columns:

        alternatives[fund.columns[x]] = fund[fund.columns[x]]

        x += 1


alternatives.dropna(how='any', axis=0, inplace=True)
alternatives.drop({'GLD', 'SPY', 'hedge funds'}, axis=1, inplace=True)

# creating the allocation DataFrame which provides a desired allocation for each investment over the period of
# the backtest
allocation = pd.DataFrame(index=alternatives.index, columns=alternatives.columns)
allocation['private_credit'] = 0.4
allocation['reits'] = 0.4
allocation['TLT'] = 0.2



invested = 1000
rebal_freq = 63

dates = alternatives.index
securities = alternatives.columns

# the dollar value of the portfolio
portfolio_value = pd.DataFrame(data=None, columns=['Portfolio'], index=dates)
portfolio_value.iloc[0]['Portfolio'] = invested

# the $ value allocated in each position
positions = pd.DataFrame(data=None, columns=securities, index=dates)

# pnl_stocks will hold the net PnL Data for each stock over the entire backtest
pnl_positions = pd.DataFrame(data=0, columns=securities, index=dates)

for t in range(0, len(alternatives), rebal_freq):

    if t == 0:
        rb_day = dates[t]
    else:
        rb_day = dates[t + 1]

    # the day that we rebalance the portfolio, use this value in portfolio_value to calculate allocation
    rb_value = dates[t]

    try:
        rb_end = dates[t + rebal_freq]
    except IndexError:
        rb_end = dates[-1]

    for position in positions:
        positions.loc[rb_day: rb_end, position] = portfolio_value['Portfolio'][rb_value] * (
                allocation[position][rb_day] * np.cumprod(1 + alternatives.loc[rb_day: rb_end, position]))

        pnl_positions.loc[rb_day:rb_end, position] = (positions.loc[rb_day:rb_end, position] -
                                                      portfolio_value['Portfolio'][rb_value] * allocation[position][
                                                          rb_day]
                                                      ) + pnl_positions.loc[rb_value, position]

    portfolio_value.loc[rb_day: rb_end, 'Portfolio'] = np.nansum(positions.loc[rb_day: rb_end], axis=1)


portfolio_value.plot()
plt.show()

pnl_positions.plot()
plt.show()

# this shows the $ value in each investment - we can draw the % allocation to each investment from this
positions.plot()
plt.show()




# returns = np.cumprod(1 + alternatives, axis=0)
#
# returns.to_csv('test.csv')

# returns['mean'] = returns.mean(axis=1)
#
# returns.plot()
# plt.show()
#
#
# dd = (returns['mean'] / returns['mean'].cummax()) - 1
# dd.plot()
# plt.show()



