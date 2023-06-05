import polars as pl
from wellwellwell import analyses


def test_area_under_curve_by_sample():
    """The trapezoidal calucaltions were verified with the following tool:
    https://www.emathhelp.net/en/calculators/calculus-2/trapezoidal-rule-calculator-for-a-table
    """
    df = pl.DataFrame({
        "rlu_dx": [1, 2, 4, 8, 10, 12],
        "sample_id": ["DC2", "DC2", "DC2", "DC3", "DC3", "DC3"],
        "time": [1, 2, 3, 1, 2, 3]
    })
    df = analyses.area_under_curve_by_sample(df)
    assert df.shape == (2, 2)
    sub = df.filter(pl.col("sample_id") == "DC2")
    assert sub["auc"].to_list() == [4.5]
    sub2 = df.filter(pl.col("sample_id") == "DC3")
    assert sub2["auc"].to_list() == [20]