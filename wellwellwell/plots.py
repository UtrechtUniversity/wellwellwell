import seaborn as sns
import matplotlib.pyplot as plt
import polars as pl

uu_data_palette = [
    "#F3965E", # orange
    "#AA1555", # burgundy
    "#6E3B23", # brown
    "#24A793", # green
    "#5287C6", # blue
    "#001240", # dark blue
    "#5B2182", # purple 
    "#C00A35", # red
]

A4_SIZE = (11.7, 8.27)

colorblind_palette = sns.color_palette("colorblind", 8)

def control_auc_box_pair(df: pl.DataFrame):
    """Create a pair of boxplots side-by-side for controls accross samples
    
    The left plot has all the AUCs of the control samples.
    The right plot has the values split by sample.
    """
    sns.set_palette(uu_data_palette)
    sns.set_style('whitegrid')
    df_pd = df.to_pandas()
    fig, ax = plt.subplots(1, 2, figsize=A4_SIZE, sharey=True, width_ratios=[1, 3])
    left = sns.boxplot(data=df_pd, x="treatment", y="auc", showfliers = False, boxprops=dict(alpha=.25), ax=ax[0])
    left = sns.stripplot(data=df_pd, x="treatment", y="auc",  hue="source", size=3, ax=ax[0])
    left.set_xlabel("Treatment", fontsize=10)
    left.set_ylabel("Area Under Curve", fontsize=10)
    right = sns.boxplot(data=df_pd, x="source", y="auc", showfliers = False, boxprops=dict(alpha=.25), ax=ax[1])
    right = sns.stripplot(data=df_pd, x="source", y="auc",  hue="source", size=3, ax=ax[1])
    right.set_xlabel("Sample", fontsize=10)
    right.set_ylabel("")
    plt.xticks(rotation=90)
    sns.move_legend(right, "upper left", bbox_to_anchor=(1, 1))
    left.get_legend().remove()
    fig.suptitle("Area Under Curve of Controls for All Samples", fontsize=16)
    return fig, ax


def plate_grid_timeseries(df: pl.DataFrame):
    """Create a 12x8 grid of timeseries plots for each well in a plate"""
    sns.set_palette(uu_data_palette)
    sns.set_style('whitegrid')
    df_pd = df.to_pandas()
    grid = sns.FacetGrid(
        df_pd,
        col="position",
        row="row",
        hue="treatment",
        col_order=sorted(df["position"].unique().to_list()),
        row_order=sorted(df["row"].unique().to_list()),
    )
    grid.map(sns.lineplot, "time", "rlu_dx").add_legend()
    return grid


def auc_boxplot(df: pl.DataFrame):
    """Create a boxplot of the AUCs for all present treatments"""
    sns.set_palette(uu_data_palette)
    sns.set_style('whitegrid')
    df_pd = df.to_pandas()
    box = sns.boxplot(data=df_pd, x="treatment", y="auc", showfliers = False, boxprops=dict(alpha=.25))
    box = sns.stripplot(data=df_pd, x="treatment", y="auc",  hue="treatment", size=3)
    box.set_xlabel("Treatment", fontsize=10)
    box.set_ylabel("Area Under Curve", fontsize=10)
    box.set_title("Area Under Curve for Treatments", fontsize=16)
    sns.move_legend(box, "upper left", bbox_to_anchor=(1, 1))
    plt.xticks(rotation=90)
    return box