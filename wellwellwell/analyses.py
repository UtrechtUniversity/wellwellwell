"""
A Module containing functions for analyzing 06-well data after normalization.
Most analyses will rely on having an`rlu_dx` value. 
Each analysis must be used in isolation; you cannot chain analyses together.
"""

import numpy as np
import polars as pl


def area_under_curve_by_sample(df: pl.DataFrame) -> pl.DataFrame:
    """Compute the area under the curve for each well over time
    
    This method assumes that the input is a polars DataFrame with (at least) the following columns:
    - rlu_dx: the relative change in RLU over time
    - time: the timepoint of the measurement
    - sample_id: a unique identifier for the well
    
    The result is a DataFrame with the following columns:
    - auc: the area under the curve for the well
    - sample_id: a unique identifier for the well
    
    It can be used to create a bigger dataset by joining the resulting dataframe onto `sample_id`"""
    def auc(sample_df: pl.DataFrame) -> pl.DataFrame:
        sorted_df = sample_df.sort("time")
        result = np.trapz(sorted_df["rlu_dx"], sorted_df["time"])
        res_df = pl.DataFrame({
            "auc": [result],
            "sample_id": sorted_df["sample_id"].unique()
        })
        return res_df

    return df.groupby("sample_id").apply(auc)
