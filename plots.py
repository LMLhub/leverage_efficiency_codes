import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yaml
import sys
import leverage_efficiency.base
import leverage_efficiency.figures as figs

def main(config_file):

    # Read the config information to control what gets executed
    f = open(config_file,'r')
    config = yaml.load(f, Loader=yaml.SafeLoader)
    f.close()
    analysis_folder = config['analysis_folder']
    plots_folder = config['plots_folder']
    pairs = config['plots']['pairs']
    figures = config['plots']['figures']
    runstage = config['plots']['run']

    if runstage:
        print("\n###")
        print('Running plots.py. Generating figures in '+plots_folder)
        print("###")

        if figures['expanding windows']:
            for pair in pairs:
                outputfile = plots_folder+pair+'_lopt_exp_window.pdf'
                fig, ax = figs.fig_exp_window(analysis_folder,   pair)
                fig.savefig(outputfile, bbox_inches='tight')
                plt.close()

        if figures['expanding windows significance']:
            for pair in pairs:
                outputfile = plots_folder+pair+'_lopt_exp_window_significance.pdf'
                fig, ax = figs.fig_exp_window_significance(analysis_folder,   pair)
                fig.savefig(outputfile, bbox_inches='tight')
                plt.close()

        if figures['growth rate vs leverage']:
            for pair in pairs:
                outputfile = plots_folder+pair+'_growth_vs_leverage.pdf'
                fig, ax = figs.fig_growth_vs_leverage(analysis_folder, plots_folder, pair)
                if pair=='SP500TR-FED':
                    plt.legend(loc='lower left', bbox_to_anchor=(.3,.3))
                fig.savefig(outputfile, bbox_inches='tight')
                plt.close()

        if figures['final equity vs leverage']:
            for pair in pairs:
                outputfile = plots_folder+pair+'_final_equity.pdf'
                fig, ax = figs.fig_final_equity(analysis_folder, plots_folder, pair)
                if pair=='SP500TR-FED':
                    plt.legend(loc='lower left', bbox_to_anchor=(.0,.6))
                fig.savefig(outputfile, bbox_inches='tight')
                plt.close()

        if figures['equity trajectories']:
            for pair in pairs:
                outputfile = plots_folder+pair+'_equity_trajectories.pdf'
                fig, ax = figs.fig_equity_trajectories(analysis_folder, plots_folder, pair)
                fig.savefig(outputfile, bbox_inches='tight')
                plt.close()

        if figures['l_opt variance']:
            outputfile = plots_folder+'lopt_var.pdf'
            fig, ax = figs.fig_lopt_var(analysis_folder, plots_folder, ['SP500-FED','BTC-FED'])
            fig.savefig(outputfile, bbox_inches='tight')
            plt.close()

        if figures['fixed windows']:
            for pair in pairs:
                outputfile = plots_folder+pair+'_leverage_vary_window.pdf'
                fig, ax = figs.fig_leverage_vary_window(analysis_folder, plots_folder, pair, 1)
                fig.savefig(outputfile, bbox_inches='tight')
                plt.close()

        if figures['compare assets']:
                outputfile = plots_folder+'compare_assets.pdf'
                fig, ax = figs.fig_compare_assets(analysis_folder, plots_folder)
                fig.savefig(outputfile, bbox_inches='tight')
                plt.close()

# Execute the main() function

if __name__ == "__main__":
    # Get the name of the config file
    config_file = leverage_efficiency.base.get_config_filename(sys.argv)
    main(config_file)
