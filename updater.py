# Run the extract pipeline stage on the data to create the asset file
# data/2-intermediate/XYZ.csv
#
# Download new data into data/1-source/update/XYZ.csv It must be named XYZ.csv where XYZ
# is the key (BTC,SP500, SP500TR,BRK, FED etc) defined in the config file to refer to
# this asset. There is a script provided to automatically query Yahoo Finance for
# assets that are available there.
#
# Run the extract pipeline stage on the new data to create the asset file
# data/2-intermediate/update/XYZ.csv
#
# Run the merge script to attempt to merge data/2-intermediate/XYZ.csv with
# data/2-intermediate/update/XYZ.csv and if it succeeds, overwrite the original
# data/2-intermediate/XYZ.csv file with the updated data
#
# Run the transform pipeline stage to create the asset file
# data/4-load/XYZ.csv from the updated data/2-intermediate/XYZ.csv
#
# Switch off the extract and transform pipeline stages and run the rest of the
# pipeline. Note that the updated data will be overwritten if the extract pipeline
# stage is run again.

import argparse
import os
import yaml
from pathlib import Path
import yfinance as yf
import leverage_efficiency.data as data
import pandas as pd

def update_existing_data(existing, new, config):
  print(f"Reading {existing}")
  df_existing = pd.read_csv(Path(config["existing data folder"]) / existing)
  print(df_existing.columns)
  print(f"Reading {new}")
  df_new = pd.read_csv(Path(config["new data folder"]) / new)
  print(df_new.columns)
  return


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--config", help="Specify a yaml file with config info")
  args = parser.parse_args()

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

  # Download the data from Yahoo Finance if required
  if config_data['download new data']:
    new_data_folder = config_data['new data folder']
    tickers = config_data['tickers']
    newdata = {}
    for asset in config_data['update from YF']:
      print(f"  Downloading ticker data {tickers[asset]} for {asset}")
      ticker = yf.Ticker(tickers[asset])
      df = ticker.history(period="max")
      filename = Path(new_data_folder) / f"{asset}.csv"
      df.to_csv(filename, date_format='%Y-%m-%d')
      # Save the updated data to a csv file
      print(f"Saving {asset} data to a {filename}")

  # Get the list of files contained in config_data['new data folder']
  # Verify if the folder exists and if it checks out, the read the names of  the
  # files in the folder
  new_data_folder = config_data['new data folder']
  folder_path = Path(new_data_folder)
  if folder_path.is_dir():
    # Read the names of the files in the folder into a list
    new_file_names = [file for file in folder_path.iterdir() if file.is_file()]
  else:
    print(f"Error: {new_data_folder} is not a valid folder!")
    return

  # Get the list of files contained in config_data['existing data folder']
  # Verify if the folder exists and if it checks out, the read the names of  the
  # files in the folder
  existing_data_folder = config_data['existing data folder']
  folder_path = Path(existing_data_folder)
  if folder_path.is_dir():
    # Read the names of the files in the folder into a list
    existing_file_names = [file for file in folder_path.iterdir() if file.is_file()]
  else:
    print(f"Error: {new_data_folder} is not a valid folder!")
    return

  for asset in config_data['assets']:
    # read and process new data according to the same rules as existing data
    new_data_folder = config_data['new data folder']
    target_folder = config_data['intermediate extra data folder']
    if asset == 'BTC':
      data.extract_BTC_data(new_data_folder, target_folder, f"{asset}.csv", update=True)
    if asset == 'SP500TR':
      data.extract_SP500TR_data(new_data_folder, target_folder, f"{asset}.csv", update=True)
    if asset == 'SP500':
      data.extract_SP500_data(new_data_folder, target_folder, f"{asset}.csv", update=True)
    if asset == 'DAX':
      data.extract_DAX_data(new_data_folder, target_folder, f"{asset}.csv", update=True)
    if asset == 'BRK':
      data.extract_BRK_data(new_data_folder, target_folder, f"{asset}.csv", update=True)
    if asset == 'FED':
      data.extract_FED_data(new_data_folder, target_folder,  f"{asset}.csv", update=True)
    if  asset == 'BOE':
      data.extract_BOE_data(new_data_folder, target_folder, f"{asset}.csv", update=True)
    #if  asset == 'FEDM':
    #  data.extract_FEDM_data(new_data_folder, target_folder,  f"{asset}.csv", update=True)
    if  asset == 'IRDE':
      data.extract_IRDE_data(new_data_folder, target_folder, f"{asset}.csv", update=True)
    if  asset == 'DGS10':
      data.extract_DGS10_data(new_data_folder, target_folder, f"{asset}.csv", update=True)
    if  asset == 'MAD':
      #Do nothing - the MAD data is historic and should not be updated
      continue
    if  asset == 'SMT':
      data.extract_SMT_data(new_data_folder, target_folder, f"{asset}.csv", update=True)


  # Do merging of new and existing intermediate data for each asset
  existing_data_folder = config_data['intermediate data folder']
  folder_path = Path(existing_data_folder)
  if folder_path.is_dir():
    # Read the names of the files in the folder into a list
    existing_file_names = [file for file in folder_path.iterdir() if file.is_file()]
  else:
    print(f"Error: {new_data_folder} is not a valid folder!")
    return
  new_data_folder = config_data['intermediate extra data folder']
  folder_path = Path(new_data_folder)
  if folder_path.is_dir():
    # Read the names of the files in the folder into a list
    new_file_names = [file for file in folder_path.iterdir() if file.is_file()]
  else:
    print(f"Error: {new_data_folder} is not a valid folder!")
    return

  new_file_names = [item for item in new_file_names if "FEDM" not in item.name]
  existing_file_names = [item for item in existing_file_names if "FEDM" not in item.name]
  for asset in config_data['assets']:
    #print(f"Checking if an existing csv data file can be found for {asset}...")
    # Check if existing csv data file can be found and is readable
    found_new=False
    found_existing=False
    existing_data={}
    new_data={}
    for file in existing_file_names:
      name=file.name
      if asset+'.' in name and name.endswith('.csv'):
        print(f"{asset} : {file.resolve()}")
        existing_data[asset]=file
        found_existing=True
        break
    for file in new_file_names:
      name=file.name
      if asset+'.' in name and name.endswith('.csv'):
        new_data[asset]=file
        print(f"{asset} : {file.resolve()}")
        found_new=True
        break
    if not found_existing:
      print(f"No existing data file found for {asset}")
    if not found_new:
      print(f"No new data file found for {asset}")
    if found_existing and found_new:
      print(f"New and existing data available for {asset}")
      df_existing = pd.read_csv(existing_data[asset])
      df_new = pd.read_csv(new_data[asset])
      # Find start and end dates of new data
      new_start_date = df_new['date'].min()
      new_end_date = df_new['date'].max()
      existing_start_date = df_existing['date'].min()
      existing_end_date = df_existing['date'].max()
      print("New: ", new_start_date, new_end_date)
      print("Existing: ", existing_start_date, existing_end_date)
      if new_end_date >= existing_end_date and new_start_date <= existing_end_date:
        print(f"Dates for {asset} check out. Merging...")
        if existing_end_date in df_new['date'].values:
          print(f"Existing end date {existing_end_date} already exists in new data. Good!")
          to_append = df_new[df_new['date'] > existing_end_date]
          print(df_existing.tail())
          print(f"\nAppending {to_append.shape[0]} rows to existing data")
          df_existing = pd.concat([df_existing, to_append], ignore_index=True)
          print(df_existing.tail())
          # Finally write the file to the extended dataframe to the load folder
          filename = Path(config_data['intermediate data folder']) / f"{asset}.csv"
          print(f"Saving {asset} data to {filename}")
          df_existing.to_csv(filename, date_format='%Y-%m-%d', index=False)
          filename = Path(config_data['intermediate data folder']) / f"{asset}.pkl"
          print(f"Saving {asset} data to {filename}")
          df_existing['date'] = pd.to_datetime(df_existing['date'])
          df_existing.set_index('date', inplace=True, drop=True)
          df_existing.to_pickle(filename)
      else:
        print(f"Dates for {asset} do not check out. Need to investigate...")
      print("\n")
      #print(df_existing.columns)
      #print(df_new.columns)

if __name__ == "__main__":
  main()
