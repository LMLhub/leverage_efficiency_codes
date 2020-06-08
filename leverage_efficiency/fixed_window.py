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
#from scipy.optimize import minimize
import time
import pickle

# A function to round a number down to nearest multiple of a power of 10.
# Useful for constructing approximate ranges.
def my_log_round(x):
    p = int(np.floor(np.log10(abs(x))))
    return (10.0**p)*np.floor(x/(10.0**p))

# A function to generate a list of approximately logarithmically spaced
# whole numbers between start and end (inclusive)
def my_log_range(start, end, n):
    # Calculate ratio for a geometric progression
    a = np.power(end/start, 1.0/(n-1.0))
    # Calculate geometric progression
    values = [start*np.power(a, i) for i in range(0,n)]
    # Round values to nearest whole numbers
    values = np.round(values)
    # Get unique values in case there are any duplicates created by rounding
    values = list(set(values))
    # Sort the values since set() does not necessarily preserve ordering
    values = sorted(values)
    # Done
    return values

def determine_reasonable_window_lengths(ret):
    print("  Attempting to determine reasonable window lengths.")
    data_start_date = ret.index[0]
    data_end_date = ret.index[-1]
    years = len(pd.date_range(start=data_start_date,end=data_end_date,freq='Y'))
    w_min = 1.0
    w_max = my_log_round(years/2.0)
    return my_log_range(w_min, w_max, 4)


def lopt_fixed_window_size(data_folder, analysis_folder, pair):
    print('  lopt_fixed_window_size() : ', pair)
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


    if properties['windows'] == 'auto':
        window_list_years = determine_reasonable_window_lengths(rel_ret_1)
    else:
        window_list_years = properties['windows']
    window_list = [ x * 365.0 for x in window_list_years ]

    for model in properties['models']:
        lopt=pd.DataFrame(index=pd.date_range(start=min_start_date,end=max_end_date),columns=window_list)
        print('  lopt_fixed_window_size() : ', pair, 'model '+str(model))
        for window in window_list:
            print('    window = ',window)
            size=dt.timedelta(days=window)
            start_list = pd.date_range(start=min_start_date,freq='D',end=max_end_date-dt.timedelta(days=window))
            for window_start in start_list:
                time_window=[window_start,window_start+size]
                value, equity = sm.calculate_optimal_leverage(rel_ret_1,rel_ret_2,
                        time_window, model, params[asset1])
                lopt.loc[window_start+size,window]=value
        outfile = analysis_folder+pair+'-'+str(model)+'_lopt_fixed.pkl'
        lopt.to_pickle(outfile)


def main(data_folder, analysis_folder, pairs):
    for pair in pairs:
        lopt_fixed_window_size(data_folder, analysis_folder, pair)
