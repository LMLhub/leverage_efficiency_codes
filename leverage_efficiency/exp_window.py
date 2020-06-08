#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 11:17:05 2018

@author: obp48
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from . import sme_functions as sm
from . import base
import datetime as dt
import scipy.optimize
import time
import pickle

def expanding_window_fits(data_folder, analysis_folder, pair, initial_window_size=10):
    print('  expanding_window_fits() : ', pair)
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
    start_date, end_date, rel_ret_1, rel_ret_2 = sm.get_returns_data(in_file_1, in_file_2, properties)

    date1 = rel_ret_1.index[initial_window_size]
    window_end_list = pd.date_range(start=date1,end=end_date)

    for model in properties['models']:
    #for model in [1]:
        print('  expanding_window_fits() : ', pair, 'model '+str(model))
        date1 = rel_ret_1.index[initial_window_size]
        lopt=pd.Series(index=pd.date_range(start=date1,end=end_date))
        for date1 in window_end_list:
            time_window=[start_date,date1]
            value, equity = sm.calculate_optimal_leverage(rel_ret_1,rel_ret_2,time_window,
                            model, params[asset1])
            lopt[date1]=value
        outfile = analysis_folder+pair+'-'+str(model)+'_lopt_exp.pkl'
        lopt.to_pickle(outfile)



def main(data_folder, analysis_folder, pairs):
    for pair in pairs:
        expanding_window_fits(data_folder, analysis_folder, pair, 10)
