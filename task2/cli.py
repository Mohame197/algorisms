import argparse
from typing import List, Optional

from .algorithms import Trade, max_profit_divide_and_conquer, max_profit_linear
from .prices import load_prices


def describe(name: str, trade: Trade, frame) -> str:
    if trade.buy is None:
        return f"{name}: no profitable trade"
    buy_date = frame["Date"].iloc[trade.buy].date()
    sell_date = frame["Date"].iloc[trade.sell].date()
    buy_price = frame["Price"].iloc[trade.buy]
    sell_price = frame["Price"].iloc[trade.sell]
    return (
        f"{name}: buy {buy_date} at {buy_price:.2f}, "
        f"sell {sell_date} at {sell_price:.2f}, profit {trade.profit:.2f}"
    )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="maxprofit", description="Best buy and sell days in a price CSV")
    parser.add_argument("csv", help="path to a CSV file with a date column and a price column")
    parser.add_argument("--date-column", default="Date")
    parser.add_argument("--price-column", default="Close")
    args = parser.parse_args(argv)

    frame = load_prices(args.csv, args.date_column, args.price_column)
    prices = frame["Price"].tolist()
    linear = max_profit_linear(prices)
    divide = max_profit_divide_and_conquer(prices)
    print(f"{len(prices)} trading days from {frame['Date'].iloc[0].date()} to {frame['Date'].iloc[-1].date()}")
    print(describe("linear scan       ", linear, frame))
    print(describe("divide and conquer", divide, frame))
    return 0
