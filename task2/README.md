# Max Profit Finder

CS314 Analysis of Algorithms, Lecture 2 (Divide and Conquer) mini project.

Given the daily prices of a stock, find the best day to buy and the best later day to sell. The project solves it two ways and compares them:

- **Divide and conquer:** the maximum subarray of the daily price changes. The best subarray lies in the left half, in the right half, or crosses the middle. Recurrence T(n) = 2T(n/2) + Θ(n), so Θ(n log n).
- **Linear scan:** one pass that remembers the lowest price so far. Θ(n).

A brute-force Θ(n²) version is included only as an oracle for the tests.

## Structure

```
maxprofit/algorithms.py   linear scan, divide and conquer, brute force
maxprofit/prices.py       load a price CSV with pandas, generate random-walk prices
maxprofit/cli.py          command line interface
experiments/              run_experiments.py (timings) and plot.py (figures)
tests/                    pytest unit tests
data/prices.csv           AAPL daily closing prices, 2015-02-17 to 2017-02-16 (506 days)
results/results.csv       timings produced by the experiments
figures/                  plots produced by plot.py
```

## Install

```
pip install -r requirements.txt
```

## Usage

```
python -m maxprofit data/prices.csv
```

Output:

```
506 trading days from 2015-02-17 to 2017-02-16
linear scan       : buy 2016-05-12 at 90.34, sell 2017-02-15 at 135.51, profit 45.17
divide and conquer: buy 2016-05-12 at 90.34, sell 2017-02-15 at 135.51, profit 45.17
```

Use another file with `--date-column` and `--price-column` (defaults `Date` and `Close`).

From Python:

```python
from maxprofit import max_profit_linear, max_profit_divide_and_conquer

max_profit_linear([7, 1, 5, 3, 6, 4])
max_profit_divide_and_conquer([7, 1, 5, 3, 6, 4])
```

Both return `Trade(profit=5, buy=1, sell=4)`: buy on day index 1, sell on day index 4. When prices never rise they return `Trade(0.0, None, None)`.

## Tests

```
python -m pytest
```

The tests cover:

- the classic example, profit at the ends, a best trade that crosses the middle, falling and flat prices, inputs of length 0, 1 and 2, float prices;
- 500 random arrays per algorithm checked against the brute-force oracle;
- agreement of both algorithms on a 5,000-day series;
- CSV loading (sorting by date, missing values, custom columns, missing column), the price generator and the command line.

## Experiments

```
python experiments/run_experiments.py results
python experiments/plot.py results/results.csv figures
```

- Prices: a random walk with log returns N(0, 0.01²), starting at 100, fixed seed 42.
- Sizes: n = 1,000 to 1,000,000 (10 sizes).
- Each time is the median of 9 runs (5 runs above n = 100,000) of the algorithm alone, on a Python list.
- The script stops if the two algorithms return different profits.

## Data

`data/prices.csv` comes from the `finance-charts-apple.csv` file of the plotly/datasets repository on GitHub (columns `Date` and `AAPL.Close`, renamed to `Close`).
