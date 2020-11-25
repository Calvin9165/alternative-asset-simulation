from cleaning_data_functions import *
from loading_in_csv_data import alternatives
from math import sqrt
from matplotlib.colors import ListedColormap

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

max_dd = {}
cagr = {}

for i in alternatives.columns:

    max_dd.update({i: min(rolling_drawdowns(alt_cum[i]))})
    cagr.update({i: cagr_calculator(strategy_series=alt_cum[i])})

annualized_vol = alternatives.std()*sqrt(252)

vol = {}

for i in annualized_vol.index:
    vol.update({i: annualized_vol[i]})

performance = pd.DataFrame(index=[i for i in max_dd.keys()])

performance['Max Drawdown'] = max_dd.values()
performance['CAGR'] = cagr.values()
performance['Vol'] = vol.values()

fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(nrows=4, ncols=4)

ax1 = fig.add_subplot(gs[:2, :2])
ax2 = fig.add_subplot(gs[:2, 2:])
ax3 = fig.add_subplot(gs[2:, :2])
ax4 = fig.add_subplot(gs[2:, 2:])

for i in alts:
    # plot performance on first graph

    ax1.plot(alt_cum[i], label=i)

    # plot drawdowns on second graph
    ax2.plot(rolling_drawdowns(alt_cum[i]), label=i)

ax1.plot(alt_cum['SPY'], label='SPY', color='black', lw=0.5, alpha=0.75)
ax2.plot(rolling_drawdowns(alt_cum['SPY']), label='SPY', color='black', lw=0.5, alpha=0.75)

# https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html
sns.heatmap(data=matrix, annot=True, cmap='coolwarm', linecolor='black', linewidths=2, ax=ax3)

sns.heatmap(ax=ax4, data=performance, annot=True, cbar=False, cmap=ListedColormap(['#FFFFFF']), linecolor='black',
            linewidths=1)
ax4.xaxis.tick_top()
ax4.tick_params(length=0)


ax1.legend()
ax2.legend()
plt.tight_layout()
plt.show()