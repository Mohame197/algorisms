import argparse

from max_profit import divide_and_conquer, linear_scan, load_prices


def describe(name, trade, prices):
    if trade.buy_day is None:
        return f"{name}: no profitable trade"
    return (
        f"{name}: buy day {trade.buy_day} at {prices[trade.buy_day]:.2f}, "
        f"sell day {trade.sell_day} at {prices[trade.sell_day]:.2f}, "
        f"profit {trade.profit:.2f}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/prices.csv")
    parser.add_argument("--column", default="price")
    args = parser.parse_args()

    prices = load_prices(args.csv, args.column)
    print(describe("divide and conquer", divide_and_conquer(prices), prices))
    print(describe("linear scan       ", linear_scan(prices), prices))


if __name__ == "__main__":
    main()
