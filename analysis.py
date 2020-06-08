import leverage_efficiency.base
import leverage_efficiency.sme_functions as sm
import yaml
import sys

def main(config_file):

    # Read the config information to control what gets executed
    f = open(config_file,'r')
    config = yaml.load(f, Loader=yaml.SafeLoader)
    f.close()
    data_folder = config['data_folder']
    analysis_folder = config['analysis_folder']
    pairs = config['analysis']['pairs']
    runstage = config['analysis']['run']
    stages = config['analysis']['analysis stages']

    if runstage:
        print("\n###")
        print("Running analysis.py. Results will be written to ", analysis_folder)
        print("###")

        if stages['calculate grids']:
            print("\nCalculating final equity for grid of leverage values.")
            for p in pairs:
                sm.grid(data_folder, analysis_folder, p)

        if stages['fit parameters']:
            print('\nFitting parameters of leverage parabolae: fit_parameters.py')
            import leverage_efficiency.fit_parameters
            leverage_efficiency.fit_parameters.main(data_folder,analysis_folder, pairs)

        if stages['expanding window calculations']:
            print('\n Calculation of optimal leverage for expanding windows : exp_window.py.')
            import leverage_efficiency.exp_window
            leverage_efficiency.exp_window.main(data_folder,analysis_folder, pairs)

        if stages['l_opt variance calculations']:
            print('\nCalculation of variance in optimal leverage as a function of window length: lopt_var.py.')
            import leverage_efficiency.lopt_var
            leverage_efficiency.lopt_var.main(data_folder,analysis_folder, pairs)

        if stages['fixed window calculations']:
            print('\nCalculation of optimal leverage for some fixed-length windows: fixed_window.py')
            import leverage_efficiency.fixed_window
            # Define the window lengths to use for different asset pairs
            # window_lists = {
            #             'BTC-FED' : [365,2*365,3*365,4*365],
            #             'BTC-DGS10' : [365,2*365,3*365,4*365],
            #             'SP500TR-FED' : [365,5*365,10*365,20*365],
            #             'SP500TR-DGS10' : [365,5*365,10*365,20*365],
            #             'SP500-FED' : [365,5*365,10*365,20*365,40*365],
            #             'SP500-DGS10' : [365,5*365,10*365,20*365,40*365],
            #             'MAD-FEDM' : [365,2*365,3*365,4*365],
            #             'BRK-FED' : [365,5*365,10*365,20*365],
            #             'BRK-DGS10' : [365,5*365,10*365,20*365],
            #             'DAX-IRDE' : [365,5*365,10*365,20*365]
            #             }
            leverage_efficiency.fixed_window.main(data_folder,analysis_folder, pairs)


# Execute the main() function

if __name__ == "__main__":
    # Get the name of the config file
    config_file = leverage_efficiency.base.get_config_filename(sys.argv)
    main(config_file)
