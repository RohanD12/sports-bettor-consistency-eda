import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_parquet('data.parquet')

# Formatting stuff for the summary later on. This is just to make the output more readable in the console.
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.4f}'.format)

# Filter for pure sports bettors
pure_sports = df[df['topic_sport'] >= 0.99].copy()

# Drop rows with NaN values in the 'std_tx_value' column (std_tx_value is NaN for single-transaction traders)
# Also require a minimum trade count
pure_sports = pure_sports.dropna(subset=['std_tx_value'])
pure_sports = pure_sports[pure_sports['transaction_count'] >= 10]



# create a new column called bet_size_cv, which shows how erratic a trader is (larger values mean more erratic)

pure_sports['bet_size_cv'] = pure_sports['std_tx_value'] / pure_sports['mean_tx_value']

# realized that some of my traders have a mean_tx_value of 0, which is causing the bet_size_cv to be NaN or inf. Let's filter those out as well.
pure_sports = pure_sports[np.isfinite(pure_sports['bet_size_cv'])]
# also want to take out any negative edge cases
pure_sports = pure_sports[pure_sports['bet_size_cv'] >= 0]

# print data about cleaned pure sports bettors
print(pure_sports['bet_size_cv'].describe())

# split into 5 bins, based on consistency and erratics

pure_sports['consistency_bin'] = pd.qcut(pure_sports['bet_size_cv'], q=5, labels=['Most Consistent', 'Consistent', 'Neutral', 'Erratic', 'Most Erratic'])

# summary of the numbers in each bin
# PPV is the most important thing here because it shows how much money the trader is making per dollar bet. PnL is also important, but it can be skewed by a few big wins or losses. 
# Volume and transaction count are also important, but they are less important than ppv and pnl
summary = pure_sports.groupby('consistency_bin').agg(
    n_traders=('trader', 'count'),
    median_ppv=('trader_ppv', 'median'),
    mean_ppv=('trader_ppv', 'mean'),
    median_pnl=('trader_pnl', 'median'),
    mean_pnl=('trader_pnl', 'mean'),
    median_volume=('trader_volume', 'median'),
    median_tx_count=('transaction_count', 'median'),
)
print("\n=== Outcomes by betting discipline (bet-size consistency) ===")
print(summary)