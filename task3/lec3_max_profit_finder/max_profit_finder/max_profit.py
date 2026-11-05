from collections import namedtuple

import pandas as pd

Trade = namedtuple("Trade", ["buy_day", "sell_day", "profit"])
Segment = namedtuple("Segment", ["start", "end", "total"])

NO_TRADE = Trade(None, None, 0.0)


def load_prices(path, column="price"):
    frame = pd.read_csv(path)
    return frame[column].astype(float).tolist()


def daily_changes(prices):
    return [prices[k + 1] - prices[k] for k in range(len(prices) - 1)]


def max_crossing_segment(changes, lo, mid, hi):
    left_sum = float("-inf")
    running = 0.0
    left_index = mid
    for i in range(mid, lo - 1, -1):
        running += changes[i]
        if running > left_sum:
            left_sum = running
            left_index = i

    right_sum = float("-inf")
    running = 0.0
    right_index = mid + 1
    for j in range(mid + 1, hi + 1):
        running += changes[j]
        if running > right_sum:
            right_sum = running
            right_index = j

    return Segment(left_index, right_index, left_sum + right_sum)


def max_subarray(changes, lo, hi):
    if lo == hi:
        return Segment(lo, hi, changes[lo])

    mid = (lo + hi) // 2
    left = max_subarray(changes, lo, mid)
    right = max_subarray(changes, mid + 1, hi)
    crossing = max_crossing_segment(changes, lo, mid, hi)

    if left.total >= right.total and left.total >= crossing.total:
        return left
    if right.total >= left.total and right.total >= crossing.total:
        return right
    return crossing


def divide_and_conquer(prices):
    if len(prices) < 2:
        return NO_TRADE
    changes = daily_changes(prices)
    best = max_subarray(changes, 0, len(changes) - 1)
    if best.total <= 0:
        return NO_TRADE
    return Trade(best.start, best.end + 1, best.total)


def linear_scan(prices):
    if len(prices) < 2:
        return NO_TRADE
    lowest_day = 0
    best = NO_TRADE
    for day in range(1, len(prices)):
        profit = prices[day] - prices[lowest_day]
        if profit > best.profit:
            best = Trade(lowest_day, day, profit)
        if prices[day] < prices[lowest_day]:
            lowest_day = day
    return best


def brute_force(prices):
    best = NO_TRADE
    for buy in range(len(prices) - 1):
        for sell in range(buy + 1, len(prices)):
            profit = prices[sell] - prices[buy]
            if profit > best.profit:
                best = Trade(buy, sell, profit)
    return best
