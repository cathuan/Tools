# PerformanceAnalysis

What are the questions we always ask when we analyze the performance of a strategy?
+ What's the average daily pnl
+ QQPlot or F-test to see whether the return is normal distribution or not (Normal test from scipy package)
+ What's the daily return in bps
+ What's the maximum daily pnl, or the distribution of daily pnl
+ What's the maximum drawdown
+ What's the sharpe ratio
+ What's the daily delta (so analyzing hedge cost and difficuity)
+ What's the absolute daily delta
- What's the daily number of trades
- Split data by symbols and see what's the maximum pnl of symbols
    - The reason of doing this is to test whether the pnl highly depends one of the symbol
    - Remove one of the symbol and see whether this result is still good
- Prove of performance is better than random walk (average > 0)
- Smoothness of params grid search result

# Basic required to test the program

Need to create a function to automatically generate fake pnl data
- index
    - date
    - symbol
- columns
    - Info, price; Info, probs; Info, volume
    - Pnl, pnl
    - Delta, delta
    - Side, trade
