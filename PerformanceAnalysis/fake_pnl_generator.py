import numpy as np
import pandas as pd
import datetime


# Fake symbols look like TSE symbols
def fake_symbol_generator():
    n_symbols = 100
    symbols = []
    for _ in range(n_symbols):
        symbol = str(np.random.randint(1000, 10000)) + ".T"
        symbols.append(symbol)
    return symbols


# Get date range
def dates_generator(n_days):

    n_days = 200
    dates = []
    current_date = datetime.date(2016, 1, 1)
    one_day = datetime.timedelta(days=1)
    for _ in range(n_days):
        dates.append(current_date)
        current_date += one_day
    return dates


def fake_price_generator():

    n_days = 200
    dates = dates_generator(n_days)
    symbols = fake_symbol_generator()

    dfs = []
    for symbol in symbols:
        df = pd.DataFrame((np.random.normal(0, 0.02, 200) + 1).cumprod() * 1000)
        df.column = ["price"]
        df.loc[:, "date"] = dates
        df.loc[:, "symbol"] = symbol
        dfs.append(df)
    prices = pd.concat(dfs, axis=0).set_index(["date", "symbol"])
    prices.columns = ["price"]
    return prices


def fake_strategy_output(prices):

    def trade(prob):
        if prob > 2./3:
            return 1
        elif prob < 1./3:
            return -1
        else:
            return 0

    dfs = []
    prices = prices.reset_index()
    symbols = set(prices["symbol"])
    for symbol in symbols:
        df = prices[prices["symbol"] == symbol]
        probs = np.random.random(len(df))
        df.loc[:, "probs"] = probs
        df.loc[:, "trade"] = df["probs"].apply(trade)
        df.loc[:, "volume"] = np.random.randint(100, 300, len(df))
        df.loc[:, "pnl"] = (df["price"].shift(-1) - df["price"]) * df["trade"] * df["volume"]
        df.loc[:, "delta"] = df["price"] * df["volume"] * df["trade"]
        df = df[df["trade"] != 0]
        dfs.append(df.dropna())
    df_trades = pd.concat(dfs, axis=0)
    df_trades = df_trades.set_index(["date", "symbol"])
    df_trades.columns = pd.MultiIndex.from_tuples([("Info", "price"), ("Info", "probs"), ("Side", "trade"),
                                                   ("Pnl", "pnl"), ("Info", "volume"), ("Delta", "delta")])
    return df_trades


if __name__ == "__main__":

    prices = fake_price_generator()
    df = fake_strategy_output(prices)
    assert False
