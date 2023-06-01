import tempfile

from wellwellwell import ingest

wide_format_space_separated = """
Well PlateID LineID Day Experiment Treatment 0 2.5 5
A:1 platex line1 1 exp1 booptreat 1 2 3
A:2 platex line1 1 exp1 booptreat 4 5 6
""".strip()


def test_wide_format_ingest_correctly_ingests_data():
    with tempfile.NamedTemporaryFile(mode="w", delete=True) as f:
        f.write(wide_format_space_separated)
        f.flush()
        df = ingest.read_well_wide_timeseries(f.name)
    assert df.shape == (6, 11)