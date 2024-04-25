import matplotlib.pyplot as plt
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
    source_folder = config['source data folder']
    source_filenames = config['source data filenames']
    with open(source_filenames, 'r') as f:
        source_filenames = yaml.load(f, Loader=yaml.SafeLoader)
    sourcedata = source_filenames['file names']
    target_folder = config['intermediate data folder']
    runstage = config['data processing stages']['run extract']
    assets = config['data processing stages']['assets']
    daily_interest_rates = config['data processing stages']['daily interest rates']
    monthly_interest_rates = config['data processing stages']['monthly interest rates']

    all_keys = assets + daily_interest_rates + monthly_interest_rates

    if runstage:
        print("\n###")
        print("Running extract.py. Results will be written to ", target_folder)
        print("###")
        # Extract source data and assemble into input files.
        if 'BTC' in all_keys:
            data.extract_BTC_data(source_folder, target_folder, sourcedata['BTC'])
        if 'SP500TR' in all_keys:
            data.extract_SP500TR_data(source_folder, target_folder, sourcedata['SP500TR'])
        if 'SP500' in all_keys:
            data.extract_SP500_data(source_folder, target_folder, sourcedata['SP500'])
        if 'DAX' in all_keys:
            data.extract_DAX_data(source_folder, target_folder, sourcedata['DAX'])
        if 'BRK' in all_keys:
            data.extract_BRK_data(source_folder, target_folder, sourcedata['BRK'])
        if 'FED' in all_keys:
            data.extract_FED_data(source_folder, target_folder, sourcedata['FED'])
        if 'BOE' in all_keys:
            data.extract_BOE_data(source_folder, target_folder, sourcedata['BOE'])
        if 'FEDM' in all_keys:
            data.extract_FEDM_data(source_folder, target_folder, sourcedata['FEDM'])
        if 'IRDE' in all_keys:
            data.extract_IRDE_data(source_folder, target_folder, sourcedata['IRDE'])
        if 'DGS10' in all_keys:
            data.extract_DGS10_data(source_folder, target_folder, sourcedata['DGS10'])
        if 'MAD' in all_keys:
            data.extract_Madoff_data(source_folder, target_folder, sourcedata['MAD'])
        if 'SMT' in all_keys:
            data.extract_SMT_data(source_folder, target_folder, sourcedata['SMT'])

# Execute the main() function

if __name__ == "__main__":
    # Get the name of the config file
    config_file = leverage_efficiency.base.get_config_filename(sys.argv)
    main(config_file)
