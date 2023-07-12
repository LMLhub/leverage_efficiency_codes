import pandas as pd
import numpy as np
import requests
from io import StringIO
import yfinance as yf
import datetime
from . import base
import leverage_efficiency.sme_functions as sme

# Functions to open source data files shipping with repository to create
# standard data to load into the pipeline. These are hardcoded since we are using
# historical data from various sources in different formats. All should
# return a dataframe containing a single 'level' column with a datetime
# index called 'date'

# There is a problem with dates prior to 1969 being parsed as future dates
def fix_date(x):
    if x.year > 2020:
        year = x.year - 100
    else:
        year = x.year
    return datetime.date(year,x.month,x.day)

def standardise_columns(df, date_format, columns=['date','level'], fix_dates=False):
    # Standardise the column names and index
    df.columns = columns
    df['date'] = pd.to_datetime(df.date,format=date_format).dt.date
    if fix_dates:
        df['date'] = df['date'].apply(fix_date)
    df.set_index(pd.DatetimeIndex(df['date']), inplace=True, drop=True)
    df.sort_index(inplace=True)
    df.drop('date', axis=1, inplace=True)
    return df

def standardise_index(df, fill_method='forward fill'):
    # Some data has values only on trading days or monthly. Interpolate it to
    # calendar days
    df = df.reindex(pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq='1D'))
    # Fill any NaNs that have been introduced by the reindexing
    if fill_method == 'forward fill':
        df['level'] = df['level'].fillna(method='ffill')
    elif fill_method == 'interpolate':
        df.interpolate(method='linear', inplace=True)
    else:
        print("  Error: unknown value '+fill_method+ ' for fill_method.")

    # Need set the name of the new index
    df.index = df.index.rename('date')
    return df

def extract_BTC_data(source_folder, target_folder):
    print("  Extracting BTC data.")
    # Bitcoin Price Index from Coindesk
    inputfile1 = source_folder+'BPI_2010-07-18_2018-04-06_Coindesk.csv'
    date_format1 = '%Y-%m-%d %H:%M:%S'
    # BTC-USC FX pair from Yahoo Finance
    inputfile2 = source_folder+'BTC-USD_2014-09-17_2020-05-01_YF.csv'
    date_format2 = '%Y-%m-%d'
    # Need to specify the date format used by these files

    # Output files
    outputfile = target_folder+'BTC'

    # Read in the raw data
    df1 = pd.read_csv(inputfile1, skipfooter=3, engine='python')
    df2 = pd.read_csv(inputfile2)

    # Standardise the column names and indices
    df1 = standardise_columns(df1, date_format1)
    df1 = standardise_index(df1)
    df2 = standardise_columns(df2, date_format2)
    df2 = standardise_index(df2)

    # Splice these timeseries together at these dates:
    d1 = datetime.date(2014, 9, 16)
    d2 = datetime.date(2014, 9, 17)
    # Append the relevant slice of df2 to the relevant slice of df1
    #df3 = df1.loc[:d1].append(df2.loc[d2:])
    df3 = pd.concat([ df1.loc[:d1], df2.loc[d2:] ])

    # Write output
    df3.to_csv(outputfile+'.csv')
    df3.to_pickle(outputfile+'.pkl')

def extract_SP500TR_data(source_folder, target_folder):
    print("  Extracting SP500 TR data.")
    # SP500 Total Return index from Yahoo Finance
    inputfile = source_folder+'SP500TR_1988-01-04_2020-04-30_YF.csv'
    # Need to specify the date format used by these files
    date_format = '%Y-%m-%d'
    # Output file
    outputfile = target_folder+'SP500TR'

    # Read in raw data
    df = pd.read_csv(inputfile)[['Date','Close']]

    # Standardise the column names and index
    df = standardise_columns(df, date_format)
    df = standardise_index(df)

    # Write output
    df.to_csv(outputfile+'.csv')
    df.to_pickle(outputfile+'.pkl')

def extract_SP500_data(source_folder, target_folder):
    print("  Extracting SP500 data.")
    # SP500 index from Yahoo Finance
    inputfile = source_folder+'SP500_1927-12-31_2020-05-14.csv'
    # Need to specify the date format used by these files
    date_format = '%Y-%m-%d'
    # Output file
    outputfile = target_folder+'SP500'

    # Read in raw data
    df = pd.read_csv(inputfile)[['Date','Close']]

    # Standardise the column names and index
    df = standardise_columns(df, date_format, fix_dates=True)
    df = standardise_index(df)

    # Write output
    df.to_csv(outputfile+'.csv')
    df.to_pickle(outputfile+'.pkl')

def extract_DAX_data(source_folder, target_folder):
    print("  Extracting DAX data.")
    # DAX index from Yahoo Finance
    inputfile = source_folder+'DAX_1987-12-30_2020-04-30_YF.csv'
    # Need to specify the date format used by this file
    date_format = '%Y-%m-%d'
    # Output file
    outputfile = target_folder+'DAX'

    # Read in raw data
    df = pd.read_csv(inputfile)[['Date','Close']]

    # Standardise the column names and index
    df = standardise_columns(df, date_format)
    df = standardise_index(df)

    # Write output
    df.to_csv(outputfile+'.csv')
    df.to_pickle(outputfile+'.pkl')

def extract_BRK_data(source_folder, target_folder):
    print("  Extracting BRK data.")
    # Berkshire share price from Yahoo Finance
    inputfile = source_folder+'BRK_1980-03-17_2020-04-30_YF.csv'
    # Need to specify the date format used by this file
    date_format = '%Y-%m-%d'
    # Output file
    outputfile = target_folder+'BRK'

    # Read in raw data
    df = pd.read_csv(inputfile)[['Date','Close']]

    # Standardise the column names and index
    df = standardise_columns(df, date_format)
    df = standardise_index(df)

    # Write output
    df.to_csv(outputfile+'.csv')
    df.to_pickle(outputfile+'.pkl')

# OLD: def extract_FED_data(source_folder, target_folder):
#     print("Extracting FED data.")
#     # Federal overnight rates from FRED
#     inputfile = source_folder+'FED_1954-07-01_2020-03-01-FRED.csv'
#     # Need to specify the date format used by this file
#     date_format = '%Y-%m-%d'
#     # Output file
#     outputfile = target_folder+'FED'

#     # Read in raw data
#     df = pd.read_csv(inputfile)

#     # Standardise the column names and index
#     df = standardise_columns(df, date_format)
#     df = standardise_index(df, fill_method='interpolate')

#     # Write output
#     df.to_csv(outputfile+'.csv')
#     df.to_pickle(outputfile+'.pkl')

def extract_FED_data(source_folder, target_folder):
    print("  Extracting FED data.")
    # Federal overnight rates from https://t.co/FDm5p3P828?amp=1
    inputfile1 = source_folder+'FED_1927-12-30_2020-05-14.csv'
    date_format1 = '%Y%m%d'
   # Federal overnight rates from FRED
    inputfile2 = source_folder+'FED_1954-07-01_2020-03-01-FRED.csv'
    # Need to specify the date format used by this file
    date_format2 = '%Y-%m-%d'
    # Output file
    outputfile = target_folder+'FED'

    # Read in raw data
    df1 = pd.read_csv(inputfile1,skiprows=5,skipfooter=1,engine='python',usecols=[0,4])
    df2 = pd.read_csv(inputfile2)

    # Standardise the column names and index
    df1 = standardise_columns(df1, date_format1)
    df1 = standardise_index(df1)
    df2 = standardise_columns(df2, date_format2)
    df2 = standardise_index(df2)

    #Rates in this data set are quoted as daily percentage returns for trading days.
    #This needs to be converted to annual interest rates in percent.
    #Technically, they're quoted to reproduce a monthly return by compounding
    #the trading days in the relevant month but it's all very rough anyway,
    #and for now we pretend each month has the same number of trading days.
    df1 = 100*(np.power((1+df1/100),252.75)-1)

    # Splice these timeseries together at these dates:
    d1 = datetime.date(1954,6,30)
    d2 = datetime.date(1954,7,1)
    # Append the relevant slice of df2 to the relevant slice of df1
    #df3 = df1.loc[:d1].append(df2.loc[d2:])
    df3=pd.concat([df1.loc[:d1],df2.loc[d2:]])

    # Write output
    df3.to_csv(outputfile+'.csv')
    df3.to_pickle(outputfile+'.pkl')

def extract_FEDM_data(source_folder, target_folder):
    print("  Extracting FED monthly data.")
    # Federal overnight rates from FRED
    inputfile = source_folder+'FED_1954-07-01_2020-03-01-FRED.csv'
    # Need to specify the date format used by this file
    date_format = '%Y-%m-%d'
    # Output file
    outputfile = target_folder+'FEDM'

    # Read in raw data
    df = pd.read_csv(inputfile)

    # Standardise the column names and index
    df = standardise_columns(df, date_format)
    df = standardise_index(df, fill_method='interpolate')

    # Write output
    df.to_csv(outputfile+'.csv')
    df.to_pickle(outputfile+'.pkl')

def extract_DGS10_data(source_folder, target_folder):
    print("  Extracting DGS10 data.")
    # 10-Year Treasury Constant Maturity Rates from FRED
    inputfile = source_folder+'DGS10_1962-01-02_2020-05-07_FRED.csv'
    # Need to specify the date format used by this file
    date_format = '%Y-%m-%d'
    # Output file
    outputfile = target_folder+'DGS10'

    # Read in raw data
    df = pd.read_csv(inputfile)

    # This data file contains some '.'s in the level column that need to be
    # filtered out
    df = df[~(df['DGS10']=='.')]
    df['DGS10'] = df['DGS10'].astype(float)

    # Standardise the column names and index
    df = standardise_columns(df, date_format)
    df = standardise_index(df, fill_method='forward fill')

    # Write output
    df.to_csv(outputfile+'.csv')
    df.to_pickle(outputfile+'.pkl')

def extract_IRDE_data(source_folder, target_folder):
    print("  Extracting German IR data.")
    # SP500 Total Return index from Yahoo Finance
    inputfile = source_folder+'IRDE_1960-01-01_2020-03-01-FRED.csv'
    # Need to specify the date format used by this file
    date_format = '%Y-%m-%d'
    # Output file
    outputfile = target_folder+'IRDE'

    # Read in raw data
    df = pd.read_csv(inputfile)

    # Standardise the column names and index
    df = standardise_columns(df, date_format)
    df = standardise_index(df, fill_method='interpolate')

    # Write output
    df.to_csv(outputfile+'.csv')
    df.to_pickle(outputfile+'.pkl')

def extract_Madoff_data(source_folder, target_folder):
    print("  Extracting Madoff data.")
    # Madoff data
    inputfile = source_folder+'MAD_1990-01-01_2005-05-01_DU.csv'
    # Need to specify the date format used by this file
    date_format = '%d/%m/%y'
    # Output file
    outputfile = target_folder+'MAD'

    # Read in raw data
    df = pd.read_csv(inputfile, header=None)

    # Standardise the column names and index
    df = standardise_columns(df, date_format, columns=['date','return'])

    # This data file doesn't contain prices, only percentage returns so
    # we will not need to calculate returns at the next pipeline
    # stage. We do however need to convert the percentage returns to relative
    # returns:
    df['return'] = df['return']/100.0+1.0
    # Write output
    df.to_csv(outputfile+'.csv')
    df.to_pickle(outputfile+'.pkl')

def extract_SMT_data(source_folder, target_folder):
    print("  Extracting SMT data.")
    # SMT Total Return data
    inputfile = source_folder+'SMT_1964-12-30_2022-03-31.xlsx'
    # Need to specify the date format used by these files
    date_format = '%d/%m/%Y'
    # Output file
    outputfile = target_folder+'SMT'

    # Read in raw data
    xl = pd.ExcelFile(str(inputfile))
    df = xl.parse('Sheet1', header=2)
    df.drop(['Unnamed: 0','Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5'], axis=1, inplace=True)
    df.rename(columns={'Name':'date', 'SCOTTISH MORTGAGE':'level'}, inplace=True)

    # Standardise the column names and index
    df = standardise_columns(df, date_format)
    df = standardise_index(df)

    # Write output
    df.to_csv(outputfile+'.csv')
    df.to_pickle(outputfile+'.pkl')

# Functions to transform intermediate data into input format
def prepare_input_asset_data(source_folder, target_folder, tag):
    inputfile = source_folder+tag+'.pkl'
    outputfile = target_folder+tag
    df = pd.read_pickle(inputfile)

    # If return is not already present, calculate it and add it as a new column
    if not 'return' in df.columns:
        print(" ",tag + ': Calculating return.')
        df['return'] = sme.price_to_return(df['level'])
        # Drop the first line since it will be NaN due to shift operation
        df.drop(df.index[0], inplace=True)

    # Perform some simple quality checks on the data before allowing it to
    # proceed
    if not base.input_sanity_checks(df):
        print(" ", tag, ": Input data checks failed - you will probably have problems later.")
    else:
        print(" ", tag, ": Input data checks passed.")

    # Save the data
    df.to_csv(outputfile+'.csv')
    df.to_pickle(outputfile+'.pkl')

def prepare_input_interest_rate_data(source_folder, target_folder, tag, freq='daily'):
    inputfile = source_folder+tag+'.pkl'
    outputfile = target_folder+tag
    df = pd.read_pickle(inputfile)

    # For interest rate data, the 'level' is assumed to be quoted as an annual
    # rate of return. Convert these annual rates to daily returns

    if freq =='daily':
        print(" ", tag + ': Converting annual rates to daily returns.')
        df['return'] = np.power(1.0+(df['level']/100.0),1./360.0)
    elif freq == 'monthly':
        print(" ", tag + ': Converting annual rates to monthly returns.')
        df['return'] = np.power(1.0+(df['level']/100.0),1./12.0)

    # Perform some simple quality checks on the data before allowing it to
    # proceed
    if not base.input_sanity_checks(df):
        print(" ", tag, ": Input data checks failed - you will probably have problems later.")
    else:
        print(" ", tag, ": Input data checks passed.")


    # Save the data
    df.to_csv(outputfile+'.csv')
    df.to_pickle(outputfile+'.pkl')

# Functions to download new data to update
def download_yahoo(tickers, end_date=None):
    data = {}
    for t in tickers:
        print("  Downloading data for ", t)
        ticker = yf.Ticker(t)
        data[t] = ticker.history(period="max")

    # Combine these into a single dataframe
    df=data[tickers[0]]['Close']
    for t in tickers[1:]:
        df = pd.merge(df, data[t]['Close'], on='Date', how='outer')

    # Rename the columns
    df.columns=tickers
    return df

def download_csv(data_url, old_column_names, new_column_names, header=0):
    req = requests.get(data_url, verify=False)
    data = pd.read_csv(StringIO(req.text), header=header)
    df=data[old_column_names]
    df.columns = new_column_names
    df.set_index('Date', drop=True, inplace=True)
    return df
