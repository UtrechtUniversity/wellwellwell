"""
A module for all methods related to normalizing RLU values and attaching other useful information to the data.

Each method assumes that the input is a polars DataFrame with the following columns:
- source: the name of the file the data came from
- time: the timepoint of the measurement
- well: the well position on the plate
- sample_id: a unique identifier for the well
- rlu: the RLU value for the well at the given timepoint
- position: the position of the well on the plate (1-12)
- row: the row of the well on the plate (A-H)
"""
import polars as pl


def sample_rlu_dx(df: pl.DataFrame) -> pl.DataFrame:
    """A normalization to account for high variability of values on a single plate

    Consider the following data:

    sample_id | time | rlu
    ----------------------
    DC2       | 1    | 100
    DC2       | 2    | 200
    DC2       | 3    | 300
    DC3       | 1    | 1000
    DC3       | 2    | 2000
    DC3       | 3    | 3000

    Samples DC2 and DC3 have the same relative progression, however the absolute values are in different orders of magnitude. This method normalizes the data to account for this.
    Note that it is not uncommon to see these differences as RLU units are not standardized, meaning there is a lot variation between different instruments and even different runs on the same instrument.

    The method of normalization is to compute the total relative change per sample, so the above table would get translated to something like:
    sample_id | time | rlu  | rlu_dx
    --------------------------------
    DC2       | 1    | 100  | 1
    DC2       | 2    | 200  | 2
    DC2       | 3    | 300  | 3
    DC3       | 1    | 1000 | 1
    DC3       | 2    | 2000 | 2
    DC3       | 3    | 3000 | 3
    """
    def compute_dx(sample_df: pl.DataFrame) -> pl.DataFrame:
        """Compute the relative change for a single sample"""
        return (
            sample_df
            .sort("time")
            .with_columns(
                (pl.col("rlu") / pl.col("rlu").first()).alias("rlu_dx") 
                
            )
        )
    return (
        df
        .groupby("sample_id")
        .apply(compute_dx)
    )


def plate_control_background(df: pl.DataFrame, control_df: pl.DataFrame, columns=["rlu", "rlu_dx"]) -> pl.DataFrame:
    """Subtract the background of the control from the data in the provided columns

    This normalization is useful to provide relative comparisons to an untreated or negative control. Consider the following data:
    sample_id | time | rlu | rlu_dx
    -------------------------------
    DC2       | 1    | 100 | 1
    DC2       | 2    | 200 | 2
    DC2       | 3    | 300 | 3
    Control   | 1    | 10  | 1
    Control   | 2    | 15  | 1.5
    Control   | 3    | 17  | 1.7

    After this normalization, the data would look like:
    sample_id | time | rlu | rlu_dx
    -------------------------------
    DC2       | 1    | 90  | 0
    DC2       | 2    | 185 | 0.5
    DC2       | 3    | 283 | 1.3
    Control   | 1    | 0   | 0
    Control   | 2    | 0   | 0
    Control   | 3    | 0   | 0

    The normalization takes place on the plate level. So if there are multiple plates, the control background will be subtracted from each plate separately.
    """
    control_means = (
        control_df
        .groupby(["source", "time"])
        .mean()
    )
    for column in columns:
        control_means = control_means.with_columns(pl.col(column).alias(f"control_mean_{column}"))
    control_means = control_means.drop(columns + ["sample_id", "well", "position", "row"])
    joined = df.join(control_means, on=["source", "time"], how="left")
    for column in columns:
        joined = joined.with_columns(
            (pl.col(column) - pl.col(f"control_mean_{column}")).alias(column)
        )
    return joined.drop([f"control_mean_{col}" for col in columns])


def plate_control_fold_change(df: pl.DataFrame, control_df: pl.DataFrame, columns=["rlu", "rlu_dx"]) -> pl.DataFrame:
    """Use the background of the control  to divide the value from the data in the provided columns

    This normalization is useful to provide relative comparisons to a control. Unlike the background method, this can be used to evaluate treated controls too. Consider the following data:
    sample_id | time | rlu | rlu_dx
    -------------------------------
    DC2       | 1    | 100 | 1
    DC2       | 2    | 200 | 2
    DC2       | 3    | 300 | 3
    Control   | 1    | 10  | 1
    Control   | 2    | 15  | 1.5
    Control   | 3    | 17  | 1.7

    After this normalization, the data would look like:
    sample_id | time | rlu | rlu_dx
    -------------------------------
    DC2       | 1    | 10  | 0
    DC2       | 2    | 13.3| 0.5
    DC2       | 3    | 17.6| 1.76
    Control   | 1    | 1   | 1
    Control   | 2    | 1   | 1
    Control   | 3    | 1   | 1

    The normalization takes place on the plate level. So if there are multiple plates, the control division by the control will occur on each plate separately.
    """
    control_means = (
        control_df
        .groupby(["source", "time"])
        .mean()
    )
    for column in columns:
        control_means = control_means.with_columns(pl.col(column).alias(f"control_mean_{column}"))
    control_means = control_means.drop(columns + ["sample_id", "well", "position", "row"])
    joined = df.join(control_means, on=["source", "time"], how="left")
    for column in columns:
        joined = joined.with_columns(
            (pl.col(column) / pl.col(f"control_mean_{column}")).alias(column)
        )
    return joined.drop([f"control_mean_{col}" for col in columns])
