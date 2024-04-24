import argparse
import os
import yaml
from pathlib import Path


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

  # Get the list of files contained in config_data['source data folder']
  # Verify if the folder exists and if it checks out, the read the names of  the
  # files in the folder
  existing_data_folder = config_data['existing data folder']
  folder_path = Path(existing_data_folder)
  if folder_path.is_dir():
    # Read the names of the files in the folder into a list
    file_names = [file.name for file in folder_path.iterdir() if file.is_file()]
  else:
    print(f"Error: {existing_data_folder} is not a valid folder!")
    return

  # Do stuff for each asset
  for asset in config_data['risky assets'] + config_data['riskless assets']:
    #print(f"Checking if an existing csv data file can be found for {asset}...")
    # Check if existing csv data file can be found and is readable
    found=False
    for name in file_names:
      if asset in name and name.endswith('.csv'):
        print(f"{asset} : {name}")
        found=True
        break
    if not found:
      print(f"No matching file found for {asset}")



    # Do stuff to update the asset

    # For now, just print the asset's data


if __name__ == "__main__":
  main()
