import pytest

from maxprofit import generate_prices, load_prices


def write_csv(tmp_path, text):
    path = tmp_path / "prices.csv"
    path.write_text(text)
    return str(path)


def test_load_prices_sorts_by_date_and_renames_columns(tmp_path):
    path = write_csv(tmp_path, "Date,Close\n2024-01-03,12\n2024-01-01,10\n2024-01-02,11\n")
    frame = load_prices(path)
    assert list(frame.columns) == ["Date", "Price"]
    assert frame["Price"].tolist() == [10, 11, 12]


def test_load_prices_drops_missing_values(tmp_path):
    path = write_csv(tmp_path, "Date,Close\n2024-01-01,10\n2024-01-02,\n2024-01-03,12\n")
    frame = load_prices(path)
    assert frame["Price"].tolist() == [10, 12]


def test_load_prices_custom_columns(tmp_path):
    path = write_csv(tmp_path, "day,px\n2024-01-01,5\n2024-01-02,6\n")
    frame = load_prices(path, date_column="day", price_column="px")
    assert frame["Price"].tolist() == [5, 6]


def test_load_prices_missing_column(tmp_path):
    path = write_csv(tmp_path, "Date,Open\n2024-01-01,5\n")
    with pytest.raises(ValueError):
        load_prices(path)


def test_generate_prices_is_reproducible_and_positive():
    first = generate_prices(1000, seed=1)
    second = generate_prices(1000, seed=1)
    assert first == second
    assert len(first) == 1000
    assert first[0] == 100.0
    assert min(first) > 0


def test_generate_prices_changes_with_seed():
    assert generate_prices(100, seed=1) != generate_prices(100, seed=2)
