import random

import pytest

from maxprofit import (
    NO_TRADE,
    Trade,
    daily_changes,
    max_profit_brute_force,
    max_profit_divide_and_conquer,
    max_profit_linear,
)

ALGORITHMS = [max_profit_linear, max_profit_divide_and_conquer]


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_classic_example(algorithm):
    prices = [7, 1, 5, 3, 6, 4]
    assert algorithm(prices) == Trade(5, 1, 4)


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_profit_at_the_ends(algorithm):
    assert algorithm([1, 2, 3, 4, 5]) == Trade(4, 0, 4)


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_best_trade_crosses_the_middle(algorithm):
    prices = [9, 8, 1, 7, 8, 2]
    assert algorithm(prices) == Trade(7, 2, 4)


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_falling_prices_give_no_trade(algorithm):
    assert algorithm([9, 7, 5, 3, 1]) == NO_TRADE


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_flat_prices_give_no_trade(algorithm):
    assert algorithm([4, 4, 4, 4]) == NO_TRADE


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_short_inputs(algorithm):
    assert algorithm([]) == NO_TRADE
    assert algorithm([10]) == NO_TRADE
    assert algorithm([3, 8]) == Trade(5, 0, 1)
    assert algorithm([8, 3]) == NO_TRADE


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_float_prices(algorithm):
    prices = [10.5, 9.25, 12.0, 11.5, 14.75, 13.0]
    trade = algorithm(prices)
    assert trade.buy == 1 and trade.sell == 4
    assert trade.profit == pytest.approx(5.5)


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_does_not_modify_input(algorithm):
    prices = [5, 3, 8, 1, 9]
    copy = list(prices)
    algorithm(prices)
    assert prices == copy


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_random_inputs_match_brute_force(algorithm):
    rng = random.Random(2026)
    for _ in range(500):
        n = rng.randint(0, 40)
        prices = [rng.randint(1, 30) for _ in range(n)]
        expected = max_profit_brute_force(prices)
        result = algorithm(prices)
        assert result.profit == expected.profit
        if result.buy is not None:
            assert result.buy < result.sell
            assert prices[result.sell] - prices[result.buy] == result.profit


def test_both_algorithms_agree_on_large_input():
    rng = random.Random(7)
    prices = [100.0]
    for _ in range(5000):
        prices.append(max(1.0, prices[-1] + rng.uniform(-2.0, 2.0)))
    linear = max_profit_linear(prices)
    divide = max_profit_divide_and_conquer(prices)
    assert divide.profit == pytest.approx(linear.profit)


def test_daily_changes():
    assert daily_changes([5, 7, 4, 4]) == [2, -3, 0]
    assert daily_changes([5]) == []
