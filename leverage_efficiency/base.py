import numpy as np
import pandas as pd
import os
import yaml

def get_config_filename(argv):
    # Determine the name of the config file to be used
    filename='config_default.yaml'
    if len(argv) == 1:
        print("No config file specified. Assuming config_default.yaml")
    else:
        filename = argv[1]
        print("Using config file ", filename)

    # Check that the config file exists and is readable
    if not os.access(filename, os.R_OK):
        print("Config file ", filename, " does not exist or is not readable. Exiting.")
        exit()

    return filename

def read_model_parameters():
    # Determine the name of the config file to be used
    filename='model_parameters.yaml'

    # Check that the model parameters file exists and is readable
    if not os.access(filename, os.R_OK):
        print("  Model parameter file ", filename, " does not exist or is not readable. Exiting.")
        exit()

    # Read the data and return it
    f = open(filename,'r')
    params = yaml.load(f, Loader=yaml.SafeLoader)
    f.close()

    # Convert annual rates to daily or monthly values
    for key in params.keys():
        samples_per_annum = params[key]['samples per annum']
        annualised_long_rate = params[key]['long rate']
        annualised_short_rate = params[key]['short rate']
        params[key]['long rate'] = np.power(1.0+annualised_long_rate,1./samples_per_annum)-1.0
        params[key]['short rate'] = np.power(1.0+annualised_short_rate,1./samples_per_annum)-1.0

    return params

def set_pair_properties(folder, pair):
    # Determine the name of the file if it exists
    filename=folder+pair+'.yaml'
    # Specify default values for pair properties
    start_date = 'min'
    end_date = 'max'
    defaults = {}
    defaults['windows'] = 'auto'
    defaults['models'] = [1,2,3]
    defaults['date range'] = [start_date, end_date]


    # Check if the default override file exists. If not, return defaults, else
    # read values
    if os.access(filename, os.R_OK):
        f = open(filename,'r')
        try:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        except:
            print("  Error parsing yaml file ", filename)
            exit()
        f.close()
        print("  Using", filename, "to override default parameters for ", pair)
        if 'window sizes' in data.keys():
            defaults['windows'] = data['window sizes']
        if 'models to run' in data.keys():
            defaults['models'] = data['models to run']
        if 'dates' in data.keys():
            if 'start' in data['dates'].keys():
                start_date = data['dates']['start']
            if 'end' in data['dates'].keys():
                end_date = data['dates']['end']
            defaults['date range'] = [start_date, end_date]
            if not(start_date == 'min' and end_date =='max'):
                print('  Using custom date range: ', defaults['date range'])

    return defaults

# Various checks that the input data is clean. Try to catch common errors
# that a user might make when adding a new data file.
def input_sanity_checks(df):
    returnValue = True
    # Check that the column names are correct
    for c in df.columns:
        if not c in ['level', 'return']:
            print('  Column name ', c, ' not recognised.')
            print('  Data columns should be called "level" or "return"')
            returnValue = False

    # Check that the data is indexed by a DateTimeIndex
    if not type(df.index) == pd.DatetimeIndex:
        print('  Incorrect index. Index should be of type pandas.DatetimeIndex')
        returnValue = False

    # Check that all dates are contiguous
    est_freq = pd.infer_freq(df.index, warn=True)
    if not est_freq in ['D', 'M','MS']:
        print('  Failed to verify that data is daily or monthly.' )
        returnValue = False

    # Check that there are no non-numeric data points
    for c in df.columns:
        x = pd.to_numeric(df[c], errors='coerce').notnull().all()
        if not x:
            print('  Column ', c, ' suspected non-numeric data detected.')
            returnValue = False

    return returnValue
