import pandas as pd
import numpy as np
import leverage_efficiency.base
import leverage_efficiency.data as data
import yaml
import sys

def main(config_file):
    # Read the config information to control what gets executed
    f = open(config_file,'r')
    config = yaml.load(f, Loader=yaml.SafeLoader)
    f.close()
    source_folder = config['intermediate data folder']
    target_folder = config['data_folder']
    assets = config['data processing stages']['assets']
    runstage = config['data processing stages']['run']
    daily_interest_rates = config['data processing stages']['daily interest rates']
    monthly_interest_rates = config['data processing stages']['monthly interest rates']

    if runstage:
        print("\n###")
        print("Running transform.py. Results will be written to ", target_folder)
        print("###")
        # Transform intermediate data files into input for analysis
        for key in assets:
             data.prepare_input_asset_data(source_folder, target_folder, key)

        for key in daily_interest_rates:
             data.prepare_input_interest_rate_data(source_folder, target_folder, key)

        for key in monthly_interest_rates:
             data.prepare_input_interest_rate_data(source_folder, target_folder, key, freq='monthly')

# Execute the main() function

if __name__ == "__main__":
    # Get the name of the config file
    config_file = leverage_efficiency.base.get_config_filename(sys.argv)
    main(config_file)
