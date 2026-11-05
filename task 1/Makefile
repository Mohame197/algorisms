CXX := g++
CXXFLAGS := -std=c++17 -O2 -Wall -Wextra -Iinclude
BUILD := build

all: $(BUILD)/benchmark $(BUILD)/test_sorts

$(BUILD)/benchmark: src/benchmark.cpp include/sorts.hpp
	@mkdir -p $(BUILD)
	$(CXX) $(CXXFLAGS) $< -o $@

$(BUILD)/test_sorts: tests/test_sorts.cpp include/sorts.hpp
	@mkdir -p $(BUILD)
	$(CXX) $(CXXFLAGS) $< -o $@

test: $(BUILD)/test_sorts
	./$(BUILD)/test_sorts

run: $(BUILD)/benchmark
	@mkdir -p results
	./$(BUILD)/benchmark > results/results.csv

plot:
	python3 scripts/plot.py results/results.csv figures

clean:
	rm -rf $(BUILD)

.PHONY: all test run plot clean
