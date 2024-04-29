# Functions to handle updating of the data
import argparse
from pathlib import Path
import yaml
import yfinance as yf
import leverage_efficiency.data as data
import pandas as pd

def read_config_file():
  parser = argparse.ArgumentParser()
  parser.add_argument("--config", help="Specify a yaml file with config info")
  args = parser.parse_args()
  # Read the config file
  if args.config:
    print(f"Reading {args.config}")
    if Path(args.config).is_file():
      with open(args.config, 'r') as file:
        config_data = yaml.safe_load(file)
    else:
      print(f"Error: {args.config} does not exist!")
      return
  else:
    print("Usage: python updater.py --config <config_file.yaml>")
    return
  return config_data


def download_YF_data(config,):
    tickers = config['tickers']
    new_data_folder=config['new data folder']
    for asset in config['update from YF']:
        print(f"  Downloading ticker data {tickers[asset]} for {asset}")
        ticker = yf.Ticker(tickers[asset])
        df = ticker.history(period="max")
        filename = Path(new_data_folder) / f"{asset}.csv"
        print(f"Saving {asset} data to a {filename}")
        df.to_csv(filename, date_format='%Y-%m-%d')

    return

def extract_new_data(config):
    source_folder = config['new data folder']
    target_folder = config['intermediate data folder']
    for asset in config['assets']:
      input_file = Path(source_folder)/f"{asset}.csv"
      output_file = Path(target_folder)/f"{asset}.csv"

      if not input_file.is_file():
        print(f"Error: {input_file} does not exist!")
        return
      if not Path(target_folder).is_dir():
        print(f"Error: {target_folder} is not a valid folder!")
        return
      print(f"Extracting data from {input_file} to {output_file}")
      if asset == 'BTC':
        data.extract_BTC_data(source_folder, target_folder, f"{asset}.csv", update=True)
      if asset == 'SP500TR':
        data.extract_SP500TR_data(source_folder, target_folder, f"{asset}.csv", update=True)
      if asset == 'SP500':
        data.extract_SP500_data(source_folder, target_folder, f"{asset}.csv", update=True)
      if asset == 'DAX':
        data.extract_DAX_data(source_folder, target_folder, f"{asset}.csv", update=True)
      if asset == 'BRK':
        data.extract_BRK_data(source_folder, target_folder, f"{asset}.csv", update=True)
      if asset == 'FED':
        data.extract_FED_data(source_folder, target_folder,  f"{asset}.csv", update=True)
      if  asset == 'BOE':
        data.extract_BOE_data(source_folder, target_folder, f"{asset}.csv", update=True)
      #if  asset == 'FEDM':
      #  data.extract_FEDM_data(source_folder, target_folder,  f"{asset}.csv", update=True)
      if  asset == 'IRDE':
        data.extract_IRDE_data(source_folder, target_folder, f"{asset}.csv", update=True)
      if  asset == 'DGS10':
        data.extract_DGS10_data(source_folder, target_folder, f"{asset}.csv", update=True)
      if  asset == 'MAD':
        #Do nothing - the MAD data is historic and should not be updated
        continue
      if  asset == 'SMT':
        data.extract_SMT_data(source_folder, target_folder, f"{asset}.csv", update=True)
    return

def merge_data(config):
    source_folder_new_data = config['intermediate data folder']
    source_folder_existing_data = config['existing data folder']
    target_folder = config['existing data folder']
    for asset in config['assets']:
      input_file_new = Path(source_folder_new_data)/f"{asset}.pkl"
      input_file_existing = Path(source_folder_existing_data)/f"{asset}.pkl"
      if not input_file_new.is_file():
        print(f"Error: {input_file_new} does not exist!")
        return
      if not input_file_existing.is_file():
        print(f"Error: {input_file_existing} does not exist!")
        return
      if not Path(target_folder).is_dir():
        print(f"Error: {target_folder} is not a valid folder!")
        return
      print(f"Merging data from {input_file_new} and {input_file_existing} to {target_folder}")
      df_existing = pd.read_pickle(input_file_existing)
      df_new = pd.read_pickle(input_file_new)

      # Find start and end dates of new data
      new_start_date = df_new.index.min()
      new_end_date = df_new.index.max()
      existing_start_date = df_existing.index.min()
      existing_end_date = df_existing.index.max()
      print(f"Existing data dates: {existing_start_date} to {existing_end_date}")
      print(f"New data dates: {new_start_date} to  {new_end_date}")
      if new_end_date >= existing_end_date and new_start_date <= existing_end_date:
        print(f"Dates for {asset} check out. Merging...")
        if existing_end_date in df_new.index:
          print(f"Existing end date {existing_end_date} already exists in new data. Good!")
          to_append = df_new[df_new.index > existing_end_date]
          print(f"Appending {to_append.shape[0]} rows to existing data")
          df_existing = pd.concat([df_existing, to_append], ignore_index=False)
          # Finally write the the extended dataframe to file
          output_file = Path(target_folder)/f"{asset}.csv"
          print(f"Saving {asset} data to {output_file}\n")
          df_existing.to_csv(output_file)
          output_file = Path(target_folder)/f"{asset}.pkl"
          df_existing.to_pickle(output_file)
      else:
        print(f"Dates for {asset} do not check out. Need to investigate...")
      print("\n")

    return
