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
      df.to_csv(filename)
      # Save the updated data to a csv file
      print(f"Saving {asset} data to a {filename}")

  # Get the list of files contained in config_data['new data folder']
  # Verify if the folder exists and if it checks out, the read the names of  the
  # files in the folder
  new_data_folder = config_data['new data folder']
  folder_path = Path(new_data_folder)
  if folder_path.is_dir():
    # Read the names of the files in the folder into a list
    new_file_names = [file.name for file in folder_path.iterdir() if file.is_file()]
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
    existing_file_names = [file.name for file in folder_path.iterdir() if file.is_file()]
  else:
    print(f"Error: {new_data_folder} is not a valid folder!")
    return

  # Do stuff for each asset
  for asset in config_data['assets']:
    #print(f"Checking if an existing csv data file can be found for {asset}...")
    # Check if existing csv data file can be found and is readable
    found_new=False
    found_existing=False
    existing_data={}
    new_data={}
    for name in existing_file_names:
      if asset in name and name.endswith('.csv'):
        print(f"{asset} : {name}")
        existing_data[asset]=name
        found_existing=True
        break
    for name in new_file_names:
      if asset in name and name.endswith('.csv'):
        new_data[asset]=name
        print(f"{asset} : {name}")
        found_new=True
        break
    if not found_existing:
      print(f"No existing data file found for {asset}")
    if not found_new:
      print(f"No new data file found for {asset}")

    for asset in config_data['assets']:
      if asset in new_data and asset in existing_data:
        # Update the existing data with the new data
        print(f"Updating {existing_data[asset]} with {new_data[asset]}")
        update_existing_data(existing_data[asset], new_data[asset], config_data)

if __name__ == "__main__":
  main()
