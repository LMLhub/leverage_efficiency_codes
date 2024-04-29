# Script to manage updating of data
import leverage_efficiency.update_data as update_data
def main():
  # Get the config data
  config = update_data.read_config_file()
  if config["download new data"]:
    print("Downloading new data")
    update_data.download_YF_data(config)


  if config["extract new data"]:
    print("Extracting new data")
    update_data.extract_new_data(config)

  if config["merge new data"]:
    print("Merging data")
    update_data.merge_data(config)


if __name__ == "__main__":
  main()
