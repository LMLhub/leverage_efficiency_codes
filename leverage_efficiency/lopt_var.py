#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 11:17:05 2018

@author: obp48
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from . import base
from . import sme_functions as sm
import datetime as dt
import scipy.optimize
import time
import pickle


def lopt_variance_vs_window_size(data_folder, analysis_folder, pair, initial_window_size=10):
    print('  lopt_variance_vs_window_size() : ', pair)
    # Extract the individual asset codes from the asset pair
    asset1 = pair.split('-')[0]
    asset2 = pair.split('-')[1]

    # Read market model parameters for the risky asset
    params = base.read_model_parameters()

    # Set default properties for this pair (or read them if a file is provided
    # in the modify-defaults folder to over-ride the default properties)
    properties = base.set_pair_properties('modify-defaults/', pair)

    # Read returns data for both assets
    in_file_1=data_folder+asset1+".pkl" #risky
    in_file_2=data_folder+asset2+".pkl" #riskless
    min_start_date, max_end_date, rel_ret_1, rel_ret_2 = sm.get_returns_data(in_file_1, in_file_2, properties)

    start = rel_ret_1.index[initial_window_size]
    end = rel_ret_1.index[-1]
    if start<min_start_date:
        print("  start_date not supported by data (too early)")
    if end>max_end_date:
        print("  end_date not supported by data (too late)")

    def my_m_range(start, end, log_step):
        while start <= end:
            yield start
            start *= log_step

    def my_a_range(start, end, step):
        while start <= end:
            yield start
            start += step

    f=open(analysis_folder+'outfile.txt','w')
    lopt_var=pd.Series()

    # This line produces a hardcoded windown lenght of 17 days. Can presumably
    # be replaced by a Timedelta
    #window_size=pd.Timestamp(2010,8,5)-pd.Timestamp(2010,7,19)
    #window_size=pd.Timedelta('17 days 00:00:00')
    window_size=17*(rel_ret_1.index[1]-rel_ret_1.index[0])
    while window_size<(end-start)/2:
        lopt_0=0.0
        lopt_1=0.0
        lopt_2=0.0
        for window_start in my_a_range(start,end-window_size,window_size):
            time_window=[window_start,window_start+window_size]
            lopt, equity = sm.calculate_optimal_leverage(rel_ret_1,rel_ret_2,
                            time_window, 1 , params[asset1])
            s=str(window_start)+" "+str(lopt)+" "+str(window_size.days)+"\n"
            f.write(s)
            lopt_0+=1.0
            lopt_1+=lopt
            lopt_2+=lopt*lopt
        if np.isfinite(lopt_1):
            lopt_var[window_size]=lopt_2/lopt_0-(lopt_1/lopt_0)**2.0
        else:
            lopt_var[window_size] = np.inf
        window_size=int(1.1*window_size.days)*pd.Timedelta('1 days 00:00:00')
    f.close()
    outfile = analysis_folder+pair+'_lopt_var.pkl'
    lopt_var.to_pickle(outfile)

def main(data_folder, analysis_folder, pairs):
    for pair in pairs:
        lopt_variance_vs_window_size(data_folder, analysis_folder, pair, initial_window_size=10)
