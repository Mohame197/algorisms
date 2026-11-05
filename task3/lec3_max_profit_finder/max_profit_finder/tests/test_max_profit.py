import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from max_profit import (
    brute_force,
    daily_changes,
    divide_and_conquer,
    linear_scan,
    max_crossing_segment,
    max_subarray,
)

ALGORITHMS = [divide_and_conquer, linear_scan, brute_force]


class KnownCases(unittest.TestCase):
    def test_clrs_example(self):
        prices = [100, 113, 110, 85, 105, 102, 86, 63, 81, 101, 94, 106, 101, 79, 94, 90, 97]
        for algorithm in ALGORITHMS:
            trade = algorithm(prices)
            self.assertEqual((trade.buy_day, trade.sell_day, trade.profit), (7, 11, 43))

    def test_rising_prices(self):
        prices = [1, 2, 3, 4, 5]
        for algorithm in ALGORITHMS:
            trade = algorithm(prices)
            self.assertEqual((trade.buy_day, trade.sell_day, trade.profit), (0, 4, 4))

    def test_falling_prices(self):
        prices = [9, 7, 5, 3, 1]
        for algorithm in ALGORITHMS:
            self.assertIsNone(algorithm(prices).buy_day)
            self.assertEqual(algorithm(prices).profit, 0)

    def test_constant_prices(self):
        for algorithm in ALGORITHMS:
            self.assertEqual(algorithm([4, 4, 4, 4]).profit, 0)

    def test_two_days(self):
        for algorithm in ALGORITHMS:
            trade = algorithm([3, 8])
            self.assertEqual((trade.buy_day, trade.sell_day, trade.profit), (0, 1, 5))

    def test_single_day_and_empty(self):
        for algorithm in ALGORITHMS:
            self.assertEqual(algorithm([5]).profit, 0)
            self.assertEqual(algorithm([]).profit, 0)

    def test_profit_at_the_end(self):
        prices = [10, 9, 8, 7, 6, 20]
        for algorithm in ALGORITHMS:
            trade = algorithm(prices)
            self.assertEqual((trade.buy_day, trade.sell_day, trade.profit), (4, 5, 14))

    def test_trade_crosses_the_middle(self):
        prices = [5, 1, 3, 4, 9, 2]
        for algorithm in ALGORITHMS:
            trade = algorithm(prices)
            self.assertEqual((trade.buy_day, trade.sell_day, trade.profit), (1, 4, 8))


class Components(unittest.TestCase):
    def test_daily_changes(self):
        self.assertEqual(daily_changes([3, 5, 4, 9]), [2, -1, 5])

    def test_crossing_segment(self):
        changes = [-2, 3, -1, 4, -5]
        segment = max_crossing_segment(changes, 0, 2, 4)
        self.assertEqual((segment.start, segment.end, segment.total), (1, 3, 6))

    def test_max_subarray_single_element(self):
        segment = max_subarray([-7], 0, 0)
        self.assertEqual((segment.start, segment.end, segment.total), (0, 0, -7))


class RandomisedAgreement(unittest.TestCase):
    def test_algorithms_agree_on_random_inputs(self):
        rng = random.Random(314)
        for _ in range(500):
            n = rng.randint(0, 40)
            prices = [rng.randint(1, 60) for _ in range(n)]
            expected = brute_force(prices).profit
            self.assertEqual(divide_and_conquer(prices).profit, expected)
            self.assertEqual(linear_scan(prices).profit, expected)

    def test_returned_days_realise_the_profit(self):
        rng = random.Random(7)
        for _ in range(300):
            prices = [rng.randint(1, 100) for _ in range(rng.randint(2, 60))]
            for algorithm in (divide_and_conquer, linear_scan):
                trade = algorithm(prices)
                if trade.buy_day is None:
                    self.assertEqual(trade.profit, 0)
                else:
                    self.assertLess(trade.buy_day, trade.sell_day)
                    self.assertEqual(prices[trade.sell_day] - prices[trade.buy_day], trade.profit)

    def test_large_input_agreement(self):
        rng = random.Random(99)
        prices = [rng.randint(1, 10_000) for _ in range(20_000)]
        self.assertEqual(divide_and_conquer(prices).profit, linear_scan(prices).profit)


if __name__ == "__main__":
    unittest.main()
