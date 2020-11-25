from cleaning_data_functions import *
from loading_in_csv_data import alternatives

import pandas as pd
from pandas.plotting import table
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

alts = ['private_credit', 'reits', 'hedge funds']
non_alts = ['GLD', 'SPY', 'TLT']

# print(alternatives.head())
# print(alternatives['private_credit', 'reits', 'hedge funds', 'SPY'])

# alternatives.drop({'TLT', 'GLD'}, axis=1, inplace=True)

# alt_cum = np.cumprod(1 + alternatives, axis=0)

matrix = round(alternatives.drop({'TLT', 'GLD'}, axis=1).corr(), 2)

fig = plt.figure(figsize=(9, 6))
gs = fig.add_gridspec(nrows=4, ncols=4)

ax1 = fig.add_subplot(gs[:2, :2])
ax2 = fig.add_subplot(gs[:2, 2:])
ax3 = fig.add_subplot(gs[2:, :2])

for i in alts:
    # plot performance on first graph
    ax1.plot(np.cumprod(1 + alternatives[i]), label=i)

    # plot drawdowns on second graph
    ax2.plot(rolling_drawdowns(np.cumprod(1 + alternatives[i])), label=i)

ax1.plot(np.cumprod(1 + alternatives['SPY']), label='SPY', color='black', lw=0.5, alpha=0.75)
ax2.plot(rolling_drawdowns(np.cumprod(1 + alternatives['SPY'])), label='SPY', color='black', lw=0.5, alpha=0.75)
sns.heatmap(data=matrix, annot=True, cmap='coolwarm', linecolor='black', linewidths=2, ax=ax3)


ax1.legend()
ax2.legend()
plt.tight_layout()
plt.show()
