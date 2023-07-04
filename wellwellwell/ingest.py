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


def read_well_wide_timeseries(path: str) -> pl.DataFrame:
    """Given an input of space-separated records in wide format, return a long-format table for each well with the time and the value and position of the value on the well plate."""
    filename = Path(path).stem
    df = pl.read_csv(path, separator=" ")
    df = df.drop_nulls()
    id_vars = ["row", "position", "source", "treatment", "line_id", "experiment", "day"]
    df = (
        df
        .with_columns(
            pl.col("Well").str.slice(0, 1).alias("row"),
            pl.col("Well").str.slice(2, 3).alias("position").cast(pl.Int32),
            pl.lit(filename).alias("source"),
        )
        .rename(
            {
                "Treatment": "treatment",
                "LineID": "line_id",
                "Experiment": "experiment",
                "Day": "day",
            }
        )
        .drop(["Well", "PlateID"])
        .melt(id_vars=id_vars, variable_name="time", value_name="rlu")
        .with_columns(
            pl.col("time").cast(pl.Float32),
            pl.col("rlu").cast(pl.Int32),
            pl.concat_str(pl.col("row"), pl.col("position")).alias("well"),
            pl.concat_str(pl.col("source"), pl.lit("_"), pl.col("row"), pl.col("position")).alias("sample_id")
        )
    )
    return df


def read_well_wide_timeseries_folder(dir_path: str) -> pl.DataFrame:
    """Given a folder of well grid time series files, interpret them to a single Data Frame"""
    filenames = (os.path.join(dir_path, f) for f in os.listdir(dir_path))
    filenames = (f for f in filenames if os.path.isfile(f))
    frames = [read_well_wide_timeseries(f) for f in filenames]
    return pl.concat(frames)