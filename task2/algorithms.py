from typing import List, NamedTuple, Optional, Sequence, Tuple


class Trade(NamedTuple):
    profit: float
    buy: Optional[int]
    sell: Optional[int]


NO_TRADE = Trade(0.0, None, None)


def daily_changes(prices: Sequence[float]) -> List[float]:
    return [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]


def max_profit_linear(prices: Sequence[float]) -> Trade:
    best = NO_TRADE
    if len(prices) < 2:
        return best
    low = 0
    for day in range(1, len(prices)):
        profit = prices[day] - prices[low]
        if profit > best.profit:
            best = Trade(profit, low, day)
        if prices[day] < prices[low]:
            low = day
    return best


def _best_crossing(changes: Sequence[float], lo: int, mid: int, hi: int) -> Tuple[float, int, int]:
    total = 0.0
    left_sum = float("-inf")
    left_start = mid - 1
    for i in range(mid - 1, lo - 1, -1):
        total += changes[i]
        if total > left_sum:
            left_sum = total
            left_start = i
    total = 0.0
    right_sum = float("-inf")
    right_end = mid
    for j in range(mid, hi):
        total += changes[j]
        if total > right_sum:
            right_sum = total
            right_end = j
    return left_sum + right_sum, left_start, right_end


def _best_subarray(changes: Sequence[float], lo: int, hi: int) -> Tuple[float, int, int]:
    if hi - lo == 1:
        return changes[lo], lo, lo
    mid = (lo + hi) // 2
    best = _best_subarray(changes, lo, mid)
    crossing = _best_crossing(changes, lo, mid, hi)
    if crossing[0] > best[0]:
        best = crossing
    right = _best_subarray(changes, mid, hi)
    if right[0] > best[0]:
        best = right
    return best


def max_profit_divide_and_conquer(prices: Sequence[float]) -> Trade:
    if len(prices) < 2:
        return NO_TRADE
    changes = daily_changes(prices)
    total, start, end = _best_subarray(changes, 0, len(changes))
    if total <= 0:
        return NO_TRADE
    buy, sell = start, end + 1
    return Trade(prices[sell] - prices[buy], buy, sell)


def max_profit_brute_force(prices: Sequence[float]) -> Trade:
    best = NO_TRADE
    for buy in range(len(prices)):
        for sell in range(buy + 1, len(prices)):
            profit = prices[sell] - prices[buy]
            if profit > best.profit:
                best = Trade(profit, buy, sell)
    return best
