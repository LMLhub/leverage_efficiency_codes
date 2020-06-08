#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 10:49:42 2018

@author: obp48
"""

# if __name__ == "__main__":
#     __package__ = 'leverage_efficiency'
#     import sys
#     sys. path. append('/Users/colmconnaughton/GitHub/LML/Leverage_Efficiency/codes/codes2')

import pandas as pd
import pickle
import datetime
from . import sme_functions as sm

def write_tex(pair, fit_parameters, tex):
    tex.write("\n#####"+pair+"#####\n")
    tex.write("#start_date:\t"+str(fit_parameters['start_date'])[0:10]+'\n'\
              +'#end_date:\t'+str(fit_parameters['end_date'])[0:10]+'\n'\
              +"#years:\t"+str(round(float(fit_parameters['years']),2))+"\n"\
              +'#min_leverage:\t'+str(round(float(fit_parameters['min_leverage']),2))+'\n'\
              +'#max_leverage:\t'+str(round(float(fit_parameters['max_leverage']),2))+'\n'\
              +'#sigma_est:\t'+str(round(float(fit_parameters['sigma_est']),4))+'\n'\
              +'#mu_riskless_est:\t'+str(round(float(fit_parameters['mu_riskless_est']),4))+'\n'\
              +'#mu_excess_est:\t'+str(round(float(fit_parameters['mu_excess_est']),4))+'\n'\
              +'#g_riskless_measured:\t'+str(round(float(fit_parameters['g_riskless_measured']),4))+'\n'\
              +'#g_risky_measured:\t'+str(round(float(fit_parameters['g_risky_measured']),4))+'\n'\
              +'#lopt_1:\t'+str(round(float(fit_parameters['lopt_1']),2))+'\n'\
              +'#lopt_2:\t'+str(round(float(fit_parameters['lopt_2']),2))+'\n'\
              +'#lopt_3:\t'+str(round(float(fit_parameters['lopt_3']),2))+'\n'\
              +'#lopt_error:\t'+str(round(float(fit_parameters['lopt_error']),2))+'\n')
    tex.write("\n")

def main(data_folder, analysis_folder, pairs):
    tex=open(analysis_folder+'numbers.txt', 'w')
    for pair in pairs:
        # Actual parameter fitting gets done here:
        results = sm.fit_parameters(data_folder, analysis_folder, pair)

        # Write fitted parameters to a text file that can be read easily
        write_tex(pair, results, tex)

        # Organise the results into a dataframe
        fit_parameters=pd.DataFrame.from_dict(results,orient='index').rename(columns={0:pair})

        # Write dataframe with fitted parameters to a file for later use
        filename = analysis_folder+pair+'_prm.pkl'
        f=open(filename, 'wb')
        pickle.dump(fit_parameters, f)
        f.close()

    tex.close()
