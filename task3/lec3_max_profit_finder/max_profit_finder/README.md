# Max Profit Finder

Finds the best day to buy and the best day to sell a stock from a price CSV, using the divide-and-conquer maximum subarray algorithm and a linear scan for comparison.

## Structure

| Path | Purpose |
|---|---|
| `max_profit.py` | `divide_and_conquer`, `linear_scan`, `brute_force`, `load_prices` |
| `main.py` | Runs both algorithms on a price CSV |
| `generate_prices.py` | Creates a synthetic price CSV |
| `experiments.py` | Runtime experiments and plots |
| `tests/test_max_profit.py` | Unit tests |
| `data/prices.csv` | Sample prices (`date`, `price`) |
| `results/` | Experiment output |

## Setup

```
pip install -r requirements.txt
```

## Usage

```
python main.py
python main.py --csv data/prices.csv --column price
python generate_prices.py --days 1000 --seed 314 --output data/prices.csv
python experiments.py
```

## Tests

```
python -m unittest discover -s tests -v
```

## Complexity

| Algorithm | Time | Extra space |
|---|---|---|
| Divide and conquer | Θ(n log n) | Θ(n) |
| Linear scan | Θ(n) | Θ(1) |
| Brute force | Θ(n²) | Θ(1) |
