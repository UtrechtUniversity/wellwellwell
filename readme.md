Wellwellwelcome! In this repository you will find tools for processing 96-well plate data. 
There are 4 distinct parts to this toolset:

- data ingest: reading in raw data formats produced by various 96-well plate processors
- normalization: pre-processing of data to make it compatible for adequate analysis
- statistical analysis: computation of valuable statistics
- plots: different plots for visualizing statistics

If this software does not do what you need it to do, please make an issue!
I am looking for:
- examples of plots and graphs that you would like to recreate
- datasets that you would like to process
- statistical tests that you would like to run
- normalization methods you have seen uin the wild and would like to have critically evaluated

# Technologies
- `polars` is used for data transformations; it is a modern alternative to pandas and is very fast and efficient for both big and small datasets
- `seaborn` is used for plots; it is a very low level layer over `matplotlib` allowing for both a good degree of readability and ergonomics in creating visualizations

# Quickstarts
*In progress of writing it up...*

