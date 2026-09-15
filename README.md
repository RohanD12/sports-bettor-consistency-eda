# Sports Bettor Consistency EDA

An exploratory analysis testing whether **consistent bet sizing** ("bankroll 
management") predicts better trading outcomes among pure sports bettors in a 
prediction market dataset.

## Data
`data.parquet` — trader-level data from a prediction market platform, with 
one row per trader and features including PnL, volume, transaction count, 
topic exposure, and profit-per-volume (PPV).

## Method
1. Filter to pure sports bettors: `topic_sport >= 0.99`
2. Require at least 10 transactions per trader, so bet-size variability is 
   measurable (traders with a single transaction have no defined standard 
   deviation and are dropped)
3. Compute `bet_size_cv` = `std_tx_value / mean_tx_value` — the coefficient 
   of variation of each trader's individual bet sizes. Lower values mean more 
   consistent bet sizing; higher values mean more erratic sizing
4. Drop non-finite or negative `bet_size_cv` values (traders with a zero 
   `mean_tx_value`)
5. Split traders into 5 equal-sized groups (quintiles) by `bet_size_cv`, from 
   Most Consistent to Most Erratic
6. Compare median/mean PPV, median/mean PnL, median volume, and median 
   transaction count across the five groups
