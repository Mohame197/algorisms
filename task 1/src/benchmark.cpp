#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <vector>

#include "sorts.hpp"

namespace {

using Sorter = Stats (*)(std::vector<int>&);

struct Result {
    double time_us;
    double comparisons;
    double moves;
};

std::vector<int> make_input(const std::string& kind, int n, std::mt19937& rng) {
    std::vector<int> a(n);
    std::iota(a.begin(), a.end(), 1);
    if (kind == "reverse") {
        std::reverse(a.begin(), a.end());
    } else if (kind == "random") {
        std::shuffle(a.begin(), a.end(), rng);
    }
    return a;
}

Result measure(Sorter sort, const std::string& kind, int n, int reps,
               std::mt19937& rng) {
    std::vector<double> times;
    double comparisons = 0.0;
    double moves = 0.0;
    for (int r = 0; r < reps; ++r) {
        std::vector<int> a = make_input(kind, n, rng);
        auto t0 = std::chrono::steady_clock::now();
        Stats s = sort(a);
        auto t1 = std::chrono::steady_clock::now();
        if (!std::is_sorted(a.begin(), a.end())) {
            std::cerr << "sorting failed\n";
            std::exit(1);
        }
        times.push_back(std::chrono::duration<double, std::micro>(t1 - t0).count());
        comparisons += static_cast<double>(s.comparisons);
        moves += static_cast<double>(s.moves);
    }
    std::sort(times.begin(), times.end());
    return {times[times.size() / 2], comparisons / reps, moves / reps};
}

}

int main() {
    const std::vector<int> sizes = {100,  500,  1000, 1500, 2000, 2500,
                                    3000, 3500, 4000, 4500, 5000};
    const std::vector<std::string> kinds = {"sorted", "reverse", "random"};
    const int reps = 21;

    struct Algorithm {
        const char* name;
        Sorter sort;
    };
    const Algorithm algorithms[] = {{"insertion", insertion_sort},
                                    {"merge", merge_sort}};

    std::mt19937 rng(42);
    std::cout << "algorithm,input,n,comparisons,moves,time_us\n";
    std::cout << std::fixed << std::setprecision(1);
    for (const auto& algorithm : algorithms) {
        for (const auto& kind : kinds) {
            for (int n : sizes) {
                Result r = measure(algorithm.sort, kind, n, reps, rng);
                std::cout << algorithm.name << ',' << kind << ',' << n << ','
                          << r.comparisons << ',' << r.moves << ','
                          << std::setprecision(3) << r.time_us
                          << std::setprecision(1) << '\n';
            }
        }
    }
    return 0;
}
