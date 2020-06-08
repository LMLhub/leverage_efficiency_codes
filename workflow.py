# This function runs the pipeline.

# To set which pairs get calculated and which pipeline stages get run, edit
# the config.yaml file

import sys
import leverage_efficiency.base

def main():
    # Get the name of the config file
    config_file = leverage_efficiency.base.get_config_filename(sys.argv)

    # Extract the data from source data folder into common format
    import extract
    extract.main(config_file)

    # Update data with most recent values (optional)
    #import update       # This doesn't connect to the rest of the pipeline yet
    #update.main(config_file)

    # Calculate derived quantities like returns for input into calculations
    import transform
    transform.main(config_file)

    # Perform leverage efficiency calculations
    import analysis
    analysis.main(config_file)

    # Create figures
    import plots
    plots.main(config_file)

    # Create exact figures used in the paper
    import paper_plots
    paper_plots.main(config_file)

    # Create figures used in the EE lecture notes
    import lecture_plots
    lecture_plots.main(config_file)
# Execute the main() function

if __name__ == "__main__":
    main()
