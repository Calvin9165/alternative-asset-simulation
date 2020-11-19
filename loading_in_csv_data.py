import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from cleaning_data_functions import *

main_directory = r'C:\Users\19059\Simple Python Projects'
pc_dir = r'C:\Users\19059\Simple Python Projects\private-credit'
re_dir = r'C:\Users\19059\Simple Python Projects\private-reit-simulation'
hf_dir = r'C:\Users\19059\Simple Python Projects\hedge-fund-simulation'

r'C:\Users\19059\Simple Python Projects\private-credit'

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


fund_list = [private_credit, reits, hedge_funds]

starting = [fund.index[0] for fund in fund_list]
ending = [fund.index[-1] for fund in fund_list]

start_date = start_date_finder(dates=starting, how='newest')
end_date = end_date_finder(dates=ending, how='oldest')

date_range = pd.date_range(start_date, end_date, freq='D')

alternatives = pd.DataFrame(index=date_range)


for fund in fund_list:

    alternatives[fund.columns[0]] = fund

alternatives.dropna(how='any', axis=0, inplace=True)

returns = np.cumprod(1 + alternatives, axis=0)

returns

returns['mean'] = returns.mean(axis=1)

returns.plot()
plt.show()




