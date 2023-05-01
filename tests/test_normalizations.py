import polars as pl
from wellwellwell import normalizations as norm


def test_sample_rlu_dx_correctly_computes_dx():
    df = pl.DataFrame(
        {
            "sample_id": ["DC2", "DC2", "DC2", "DC3", "DC3", "DC3"],
            "time": [1, 2, 3, 1, 2, 3],
            "rlu": [100, 200, 300, 1000, 2000, 3000],
        }
    )

    with_dx = norm.sample_rlu_dx(df)
    dc2 = with_dx.filter(pl.col("sample_id") == "DC2").sort("time").get_column("rlu_dx").to_list()
    assert dc2 == [1, 2, 3]
    dc3 = with_dx.filter(pl.col("sample_id") == "DC3").sort("time").get_column("rlu_dx").to_list()
    assert dc3 == [1, 2, 3]


def test_plate_control_background_correctly_subtracts_background():
    df = pl.DataFrame(
        {
            "sample_id": ["DC2", "DC2", "DC2", "DC3", "DC3", "DC3"],
            "time": [1, 2, 3, 1, 2, 3],
            "rlu": [100, 200, 300, 10, 15, 17],
            "rlu_dx": [1, 2, 3, 1, 1.5, 1.7],
            "well": ["A1", "A1", "A1", "A2", "A2", "A2"],
            "position": ["1", "1", "1", "2", "2", "2"],
            "row": ["A", "A", "A", "A", "A", "A"],
            "source": ["test", "test", "test", "test", "test", "test"]
        }
    )
    control = df.filter((pl.col("position") == "2"))
    with_background = norm.plate_control_background(df, control)
    dc2 = with_background.filter(pl.col("sample_id") == "DC2").sort("time").get_column("rlu_dx").to_list()
    assert dc2 == [0, 0.5, 1.3]
    dc3 = with_background.filter(pl.col("sample_id") == "DC3").sort("time").get_column("rlu_dx").to_list()
    assert dc3 == [0, 0, 0]


def test_plate_control_fold_change_computes_correct_fold_change():
    df = pl.DataFrame(
        {
            "sample_id": ["DC2", "DC2", "DC2", "DC3", "DC3", "DC3"],
            "time": [1, 2, 3, 1, 2, 3],
            "rlu": [100, 300, 1000, 20, 40, 100],
            "rlu_dx": [1, 3, 10, 1, 2, 5],
            "well": ["A1", "A1", "A1", "A2", "A2", "A2"],
            "position": ["1", "1", "1", "2", "2", "2"],
            "row": ["A", "A", "A", "A", "A", "A"],
            "source": ["test", "test", "test", "test", "test", "test"]
        }
    )
    control = df.filter((pl.col("position") == "2"))
    with_fold_change = norm.plate_control_fold_change(df, control)
    dc2 = with_fold_change.filter(pl.col("sample_id") == "DC2").sort("time").get_column("rlu_dx").to_list()
    assert dc2 == [1, 1.5, 2]
    dc3 = with_fold_change.filter(pl.col("sample_id") == "DC3").sort("time").get_column("rlu_dx").to_list()
    assert dc3 == [1, 1, 1]