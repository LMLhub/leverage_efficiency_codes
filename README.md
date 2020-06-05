# Code repository for Leverage Efficiency paper

This project contains the python codes used to produce the data analyses and
figures in the [arxiv paper](https://arxiv.org/abs/1101.4548) on leverage efficiency. Fundamentally, the calculations involve calculating optimal leverage values for pairs of
assets, one considered "risky", the other considered "riskless".
Examples of risky assets include the SP500 index, Bitcoin, shares etc.
Examples of assets that are considered riskless include cash deposited with the
Federal Reserve, 10-year US Treasury Bonds, 10-year German Government Bonds.

# Data

Input data sets are time series containing the historical levels or returns for
various assets.
A number of publicly available data sets are provided in the folder data/1-source.
Brief instructions on how to add new data sources are at the bottom of this page.
Each asset is assigned a key code string which is use to refer to it both in
the code and in the config files that control the code.
The keys for the data sets provided with the repository and a brief description
of the corresponding data set is here:

## "Risky" assets

key | data set | Source
--- | --- | ---
SP500 | SP500 real time price index | https://finance.yahoo.com/quote/%5ESPX/history?p=%5ESPX
SP500TR | SP500 Total Return index (accounting for dividends) | https://finance.yahoo.com/quote/%5ESP500TR/history/
BTC | Bitcoin | https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD and https://www.coindesk.com/price/bitcoin
BRK | Berkshire Hathaway shares | https://finance.yahoo.com/quote/BRK-A/history?p=BRK-A
MAD | Madoff ponzi scheme | http://lml.org.uk/wp-content/uploads/2019/12/madoff.csv
DAX | DAX performance index | https://finance.yahoo.com/quote/%5EGDAXI/history?p=%5EGDAXI

## "Riskless" assets
key | data set | Source
--- | --- | ---
FED | Federal Reserve overnight rates | https://fred.stlouisfed.org/series/FEDFUNDS and https://t.co/FDm5p3P828?amp=1
DGS10 | 10-year US Treasury bonds | https://fred.stlouisfed.org/series/DGS10
IRDE | Immediate Rates: Less than 24 Hours: Call Money/Interbank Rate for Germany | https://fred.stlouisfed.org/series/IRSTCI01DEM156N

# How to run the code

The code reads in data on a number of different assets, performs various optimal
leverage calculations on asset pairs and produces some numbers and plots for
each pair.
It is structured as a pipeline with each pipeline stage performing
a distinct step in the analysis.
A master python script called `workflow.py` runs
the entire pipeline from beginning to end.
A config file is used to provide control over
the assets to be read in, the asset pairs to be analysed and the plots to be
produced without needing to edit the code.
The config file can also be used to turn on and off individual
pipeline stages.
The config files are written in [yaml](https://kapeli.com/cheat_sheets/YAML.docset/Contents/Resources/Documents/index) format.
Yaml is intended to be human-readable.
The config files should be fairly self-explanatory and editable by the user.

To run the code, run the following command in the terminal:

    python workflow.py config_default.yaml

The config file config_default contains only a single asset pair. A few other
config files are provided:

* To produce all of the figures appearing in the paper run

    ```python workflow.py config_manuscript.yaml```

* To analyse all of the data for multiple asset pairs run

    ```python workflow.py config_run_all.yaml```

  This can take a while since the variable window calculations are slow - especially for the longer time series.

* To check all of the numbers appearing in the table of values in the paper run

   ```python workflow.py config_manuscript_numbers.yaml```

   This doesn't run the variable window calculations or produce figures to avoid unnecessarily long run-time.
   The results are written in human-readable format to the file `data/5-analysis/numbers.txt`.



# Description of individual pipeline stages

The code is divided into several stages, each of which can be run independently
if you don't want to recalculate everything. Filenames for assets and pairs are
derived from the keys listed in the data tables above.

* `extract.py`

   Reads csv files containing historical asset time series data from the folder
   `data/1-source/` and converts them into a standard pandas dataframe format.
   These are then written in pickle format to the folder `data/2-intermediate/`.
   The standard dataframe has column names 'level' and/or 'return' and is indexed by a pandas `DateTimeIndex`. Missing values are interpolated so that the resulting dataframe has either daily or monthly frequency.

* `transform.py`

   Calculates the returns if only levels were provided. Converts annual rates of
   return (usually for interest rates) to daily or monthly returns. This stage reads
   the asset data from the pickles in the folder `data/2-intermediate/` and writes the final
   input data files into the folder `data/4-load/``

* `update.py`

   Not implemented yet. A future version of this will provide functionality to
   automatically update the time series with more recent data from online
   sources.

* `analysis.py`

   Performs all the calculations for the asset pairs specified in the config file.
   Asset time series are read from the folder `data/4-load/` and results of analyses
   for different pairs are written to the folder `data/5-analysis/`. This pipeline stage has a number of sub-stages that can be turned on and off:
     1. Calculate final equity values for a grid of different leverage values. This calculation is performed for each of the 3 market models (1 - simple, 2 - friction, 3 - friction + borrowing premia) discussed in the paper.
     2. Fit parameters of the leverage parabola to these equity values. This calculation is again performed for all 3 market models. The values of optimal leverage and associated parameters of interest are written in human-readable format to the file `data/5-analysis/numbers.txt`.
     3. Calculate how optimal leverage value changes as data window grows. By default this calculation is performed for all 3 market models.
     4. Calculate standard deviation of optimal leverage value as a function of data window length. This calculation is only performed for model 1.
     5. Calculate time series of "local" optimal leverage for fixed-length data windows of different duration. By default this calculation is performed for all 3 market models. The code determines some reasonable default values for the window lengths based on the lengths of the time series.

* `plots.py`

  Creates all the figures. Inputs are taken from the folder `data/5-analysis/`
  and pdf figures are written to the folder `data/6-figures/`.

# Customising and changing default behaviour

Several aspects of the calculations can be easily customised without any need to edit the code directly.
These are detailed in this section.

### Editing the market model parameters for each asset

Market model parameters such as the friction level and borrowing premia for a given asset can be changed by editing the file `model_parameters.yaml`.

### Overriding default choices for asset pairs:

Several aspects of default behaviour for any given asset pair can be changed using pair-specific files contained in the `modify-defaults/` folder.
For a pair of assets with keys 'ABC' (risky) and 'XYZ' (riskless), this file should be called `modify-defaults/ABC-XYZ.yaml`.
Examples are provided for the BTC-FED and SP500-FED pairs.
This file allows the user to

* Change the start and end dates for a given asset pair.
* Restrict which market models are run for the variable window calculations.
* Specify the data window lengths to be used for fixed window calculations.

# Details of project structure

For anyone interested in looking at the code, this map shows how the project is structured.
The idea of leverage efficiency is very simple and the core calculations require only a few lines of  code.
These core routines are contained in `leverage_efficiency.sme_functions.py`.
Most of the rest is just managing the flow of data and producing figures.

![Structure of the code](/docs/project_structure.png)


# Adding additional data for new assets

This project has not been designed to allow new data to be added without editing the code. However it should be fairly easy for a user familiar with python to add new data.
For the benefit of anyone who wants to do this, here are the steps that need to be taken:

1. Add a new csv file to the folder `data/1-source/` containing the new data. Choose a key string that will be used to identify this asset.
2. Add a new function to `leverage_efficiency/data.py` which reads this file and converts it to the standard pandas dataframe format used throughout the rest of the code. Different data sources have their own peculiarities so it is not easy to automate this. Use the examples provided. The final dataframe should have columns 'level' and/or 'return' (depending on whether the initial csv contains levels or returns) and should be indexed by a `DateTimeIndex` called 'date' which has either a daily or monthly frequency. Use interpolation to fill in weekends and holidays if the data only contains prices for trading days, for example. It is assumed that the resulting index doesn't have any gaps.
3. Add a line to `extract.py` that runs the function you created in step 2 when the key string you chose in step 1 is included in the config file.
4. Add market model parameters for the new asset to the  `model_parameters.yaml` file.
