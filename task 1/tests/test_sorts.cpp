#include <algorithm>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>

#include "sorts.hpp"

namespace {

int failures = 0;

#define CHECK(cond)                                                         \
    do {                                                                    \
        if (!(cond)) {                                                      \
            std::cerr << "FAILED " << __FILE__ << ":" << __LINE__ << "  "   \
                      << #cond << '\n';                                     \
            ++failures;                                                     \
        }                                                                   \
    } while (0)

using Sorter = Stats (*)(std::vector<int>&);

void check_sorts_like_std(Sorter sort, const std::vector<int>& input) {
    std::vector<int> expected = input;
    std::sort(expected.begin(), expected.end());
    std::vector<int> actual = input;
    sort(actual);
    CHECK(actual == expected);
}

void test_correctness(Sorter sort) {
    check_sorts_like_std(sort, {});
    check_sorts_like_std(sort, {7});
    check_sorts_like_std(sort, {2, 1});
    check_sorts_like_std(sort, {1, 2, 3, 4, 5});
    check_sorts_like_std(sort, {5, 4, 3, 2, 1});
    check_sorts_like_std(sort, {3, 3, 3, 3});
    check_sorts_like_std(sort, {2, 1, 2, 1, 2, 1});
    check_sorts_like_std(sort, {-5, 10, 0, -1, 7, -5});
    check_sorts_like_std(sort, {5, 2, 4, 6, 1, 3});
    check_sorts_like_std(sort, {25, 17, 31, 13, 2});

    std::mt19937 rng(1);
    for (int trial = 0; trial < 200; ++trial) {
        int n = static_cast<int>(rng() % 120);
        std::vector<int> a(n);
        for (int& x : a) x = static_cast<int>(rng() % 50) - 25;
        check_sorts_like_std(sort, a);
    }
}

void test_insertion_counts() {
    std::vector<int> a = {7, 3, 9, 2, 5};
    Stats s = insertion_sort(a);
    CHECK(s.comparisons == 8);
    CHECK(s.moves == 6);

    a = {4, 3, 2, 1};
    s = insertion_sort(a);
    CHECK(s.comparisons == 6);
    CHECK(s.moves == 6);

    a = {1, 2, 3, 4};
    s = insertion_sort(a);
    CHECK(s.comparisons == 3);
    CHECK(s.moves == 0);

    const int n = 100;
    std::vector<int> worst(n);
    std::iota(worst.rbegin(), worst.rend(), 1);
    s = insertion_sort(worst);
    CHECK(s.comparisons == n * (n - 1) / 2);
    CHECK(s.moves == n * (n - 1) / 2);

    std::vector<int> best(n);
    std::iota(best.begin(), best.end(), 1);
    s = insertion_sort(best);
    CHECK(s.comparisons == n - 1);
    CHECK(s.moves == 0);

    std::vector<int> empty;
    s = insertion_sort(empty);
    CHECK(s.comparisons == 0);
    CHECK(s.moves == 0);
}

void test_merge_counts() {
    std::vector<int> a = {8, 7, 4, 2, 9, 1, 5, 6};
    Stats s = merge_sort(a);
    CHECK(s.moves == 24);
    CHECK(s.comparisons <= 8 * 3);

    const int n = 1024;
    std::vector<int> big(n);
    std::iota(big.begin(), big.end(), 1);
    std::mt19937 rng(7);
    std::shuffle(big.begin(), big.end(), rng);
    s = merge_sort(big);
    CHECK(s.comparisons <= n * 10);
    CHECK(s.moves == n * 10);
}

}

int main() {
    test_correctness(insertion_sort);
    test_correctness(merge_sort);
    test_insertion_counts();
    test_merge_counts();
    if (failures == 0) {
        std::cout << "All tests passed\n";
        return 0;
    }
    std::cerr << failures << " check(s) failed\n";
    return 1;
}
