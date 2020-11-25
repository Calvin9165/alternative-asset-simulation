from cleaning_data_functions import *
from loading_in_csv_data import alternatives
from math import sqrt

import pandas as pd
from pandas.plotting import table
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

alts = ['private_credit', 'reits', 'hedge funds']
non_alts = ['GLD', 'SPY', 'TLT']

alternatives.drop({'TLT', 'GLD'}, axis=1, inplace=True)
matrix = round(alternatives.corr(), 2)

alt_cum = np.cumprod(1 + alternatives, axis=0)

fig = plt.figure(figsize=(9, 6))
gs = fig.add_gridspec(nrows=4, ncols=4)

ax1 = fig.add_subplot(gs[:2, :2])
ax2 = fig.add_subplot(gs[:2, 2:])
ax3 = fig.add_subplot(gs[2:, :2])

for i in alts:
    # plot performance on first graph

    ax1.plot(alt_cum[i], label=i)

    # plot drawdowns on second graph
    ax2.plot(rolling_drawdowns(alt_cum[i]), label=i)

ax1.plot(alt_cum['SPY'], label='SPY', color='black', lw=0.5, alpha=0.75)
ax2.plot(rolling_drawdowns(alt_cum['SPY']), label='SPY', color='black', lw=0.5, alpha=0.75)

# https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html
sns.heatmap(data=matrix, annot=True, cmap='coolwarm', linecolor='black', linewidths=2, ax=ax3)


ax1.legend()
ax2.legend()
plt.tight_layout()
# plt.show()


print(min(rolling_drawdowns(alt_cum['SPY'])))

max_dd = {}
cagr = {}

for i in alternatives.columns:

    max_dd.update({i: min(rolling_drawdowns(alt_cum[i]))})
    cagr.update({i: cagr_calculator(strategy_series=alt_cum[i])})


print(max_dd)
print(cagr)


annualized_vol = alternatives.std()*sqrt(252)

vol = {}

for i in annualized_vol.index:

    vol.update({i: annualized_vol[i]})



print(max_dd.keys())

for key, value in max_dd.items():
    print(key, value)

df = pd.DataFrame.from_dict(max_dd, orient='index')

print(df)

