#ifndef SORTS_HPP
#define SORTS_HPP

#include <vector>

struct Stats {
    long long comparisons = 0;
    long long moves = 0;
};

inline Stats insertion_sort(std::vector<int>& a) {
    Stats s;
    const int n = static_cast<int>(a.size());
    for (int j = 1; j < n; ++j) {
        int key = a[j];
        int i = j - 1;
        while (i >= 0) {
            ++s.comparisons;
            if (a[i] <= key) break;
            a[i + 1] = a[i];
            ++s.moves;
            --i;
        }
        a[i + 1] = key;
    }
    return s;
}

namespace detail {

inline void merge_range(std::vector<int>& a, std::vector<int>& buf,
                        int lo, int mid, int hi, Stats& s) {
    int i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        ++s.comparisons;
        if (a[j] < a[i]) {
            buf[k++] = a[j++];
        } else {
            buf[k++] = a[i++];
        }
        ++s.moves;
    }
    while (i < mid) {
        buf[k++] = a[i++];
        ++s.moves;
    }
    while (j < hi) {
        buf[k++] = a[j++];
        ++s.moves;
    }
    for (int t = lo; t < hi; ++t) a[t] = buf[t];
}

inline void merge_sort_range(std::vector<int>& a, std::vector<int>& buf,
                             int lo, int hi, Stats& s) {
    if (hi - lo < 2) return;
    int mid = lo + (hi - lo) / 2;
    merge_sort_range(a, buf, lo, mid, s);
    merge_sort_range(a, buf, mid, hi, s);
    merge_range(a, buf, lo, mid, hi, s);
}

}

inline Stats merge_sort(std::vector<int>& a) {
    Stats s;
    std::vector<int> buf(a.size());
    detail::merge_sort_range(a, buf, 0, static_cast<int>(a.size()), s);
    return s;
}

#endif
