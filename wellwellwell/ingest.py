"""
This module is a collection of methods to interpret multiple files with 96 well plate data and join them into a single long-fromat file.

The output for all methods yields a polars Dataframe with the following columns:
- source: the name of the file the data came from
- time: the timepoint of the measurement
- well: the well position on the plate
- sample_id: a unique identifier for the well
- rlu: the RLU value for the well at the given timepoint
- position: the position of the well on the plate (1-12)
- row: the row of the well on the plate (A-H)
"""
import polars as pl
import os
from pathlib import Path

def read_well_grid_timeseries(path: str) -> pl.DataFrame:
    """Given an input of time-based grids in CSV format, return a long-format table for each well with the time and the value and position of the value on the well plate.

    The input file is assumed to be a CSV file that follows the following structure:
    - the first row is the header denoting the 12 well columns
    - the next 8 rows denote the 8 rows of the 96 well plate
    - after each 8 row segment there is a blank row
    - each individual segment is a timepoint
    - the first column is the letter corresponding to a well row
    """
    if path.endswith(".xlsx"):
        df = pl.read_excel(path, read_csv_options={"skip_rows": 1, "has_header": False})
    else:
        raise NotImplementedError("Only Excel files are supported at this time.")
    df = df.drop_nulls()  # remove the blank rows
    df.columns = ["row"] + [str(x) for x in range(1, 13)]  # Create a custom header to suit the data format
    filename = Path(path).stem  # Extract the filename without extension and any folder path
    return (
        df
        .with_columns(
            pl.Series([1 * (n + 1) for n in range(0, int(df.height / 8)) for _ in range(8)]).alias("time"), # Add time column
            pl.lit(filename).alias("source")) # Add source column
        .melt(id_vars=["row", "source", "time"], variable_name="position", value_name="rlu")  # change orientation to long format
        .with_columns(
            pl.concat_str(pl.col("row"), pl.col("position")).alias("well"),  # Add well column
            pl.concat_str(pl.col("source"), pl.lit("_"), pl.col("row"), pl.col("position")).alias("sample_id")  # Add id column
        )
    )


def read_well_grid_timeseries_folder(dir_path: str) -> pl.DataFrame:
    """Given a folder of well grid time series files, interpret them to a single Data Frame"""
    filenames = (os.path.join(dir_path, f) for f in os.listdir(dir_path))
    frames = [read_well_grid_timeseries(f) for f in filenames]
    return pl.concat(frames)
