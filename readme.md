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

# Quickstart

There are 2 ways to get started with this project and depending on your intentions, you should pick whichever suits you best.

Use the **codespace** quickstart if:
* you just want to get to the data analysis
* you don't have a lot of python experience
* you are not excited by the prospect into running into issues with installing stuff
* you want an easily reproducible pipeline that you can share with peers and stakeholders

Use the **developer** quickstart if:
* `pip install` is not gibberish to you
* you intend to use this as only a small part of a much mroe complex pipeline

## Codespace quickstart
*TODO: instructions, video*

## Developer quickstart
1. clone the repository
2. install poetry using `pipx` (`python3 -m pipx install poetry`)
3. `poetry install` in the root directory

# Examples

* [area under curve of ros assays](https://github.com/UtrechtUniversity/uu-plants-cowper-ros-assays)
