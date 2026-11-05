from maxprofit.cli import main


def test_cli_reports_best_trade(tmp_path, capsys):
    path = tmp_path / "prices.csv"
    path.write_text("Date,Close\n2024-01-01,7\n2024-01-02,1\n2024-01-03,5\n2024-01-04,3\n2024-01-05,6\n2024-01-06,4\n")
    assert main([str(path)]) == 0
    output = capsys.readouterr().out
    assert "6 trading days" in output
    assert output.count("buy 2024-01-02 at 1.00, sell 2024-01-05 at 6.00, profit 5.00") == 2


def test_cli_reports_no_trade(tmp_path, capsys):
    path = tmp_path / "prices.csv"
    path.write_text("Date,Close\n2024-01-01,9\n2024-01-02,5\n2024-01-03,2\n")
    assert main([str(path)]) == 0
    assert capsys.readouterr().out.count("no profitable trade") == 2
