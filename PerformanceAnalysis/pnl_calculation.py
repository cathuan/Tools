import pandas as pd


def _calculate_buy_sell_pnls(df_buy, df_sell, buy_notional_per_instrument, sell_notional_per_instrumment):

    buy_num = len(df_buy)
    sell_num = len(df_sell)

    if buy_num > 0:
        buy_pnl = df_buy[("prices", "next_day_price_change")].sum() * buy_notional_per_instrument
    else:
        buy_pnl = 0

    if sell_num > 0:
        sell_pnl = df_sell[("prices", "next_day_price_change")].sum() * sell_notional_per_instrument
    else:
        sell_pnl = 0

    delta_position = buy_num * buy_notional_per_instrument - sell_num * sell_notional_per_instrument
    abs_delta_position = buy_num * buy_notional_per_instrument + sell_num * sell_notional_per_instrument

    


def delta_limit_strategy(buy_thre, sell_thre, max_delta):

    df = pd.read_csv("data.csv", header=[0, 1], index_col=[0, 1])
    df = df.reset_index()
    for date in sorted(set(df["date"])):
        df_tmp = df[df["date"] == date].set_index(["date", "symbol"]).sort([("prediction", "prob")])

        buy_num = len(df_tmp[df_tmp[("prediction", "prob")] < buy_thre])
        sell_num = len(df_tmp[df_tmp[("prediction", "prob")] > sell_thre])
        if buy_num - sell_num > max_delta:
            buy_num = max_delta + sell_num
        elif buy_num - sell_num < -max_delta:
            sell_num = max_delta + buy_num

        df_buy = df_tmp[:buy_num] if buy_num > 0 else df_tmp[:0]
        df_sell = df_tmp[-sell_num:] if sell_num > 0 else df_tmp[:0]

        pass


if __name__ == "__main__":

    delta_limit_strategy(0.495, 0.505, 2)
