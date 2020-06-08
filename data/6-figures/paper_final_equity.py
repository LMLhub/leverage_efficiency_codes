#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 18:22:45 2020

@author: obp48
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
from datetime import datetime

analysis_folder='./../5-analysis/'

# Create plot
fig, ax =plt.subplots(nrows=1, ncols=2, figsize=(9,4))
fig.tight_layout(pad=3)

#left plot
pair=['BTC','FED']
data_ID = pair[0]+'-'+pair[1]
print('Figure: fig_final_equity() : '+data_ID)

# Read in parameter information for this asset pair
f=open(analysis_folder+'best_fit_parameters.pkl', 'rb')
parameters = pickle.load(f)
f.close()
st_err=parameters[data_ID].loc['lopt_error',pair[0]]

# Read in optimal leverage values for this asset pair
returns_1=pd.read_pickle(analysis_folder+data_ID+"-1.pkl")
returns_2=pd.read_pickle(analysis_folder+data_ID+"-2.pkl")
returns_3=pd.read_pickle(analysis_folder+data_ID+"-3.pkl")
final_equity_1=np.cumprod(returns_1)[-1:].T
final_equity_2=np.cumprod(returns_2)[-1:].T
final_equity_3=np.cumprod(returns_3)[-1:].T
equity_1=np.cumprod(returns_1)
equity_2=np.cumprod(returns_2)
equity_3=np.cumprod(returns_3)

# Add lines to plot
ax[0].axvline(x=1,linestyle=':',color='red',linewidth=1.5)
ax[0].axvline(x=1+2*st_err,linestyle=':',color='pink',linewidth=1.5)
ax[0].axvline(x=1-2*st_err,linestyle=':',color='pink',linewidth=1.5)
ax[0].axhline(y=0,linestyle=':',color='grey',linewidth=.5)
ax[0].plot(final_equity_1, label='Simple',linewidth=5)
ax[0].plot(final_equity_2, label='+ friction',linewidth=3)
ax[0].plot(final_equity_3, label='+ borrowing premia',linewidth=1)
# Add remaining plot details
# #plt.xlim([final_equity_1.index.min(),final_equity_1.index.max()])
ax[0].set_xlim([-2,6])
ax[0].set_xlabel('leverage')
ax[0].set_ylabel('final equity')
ax[0].legend(loc='best', bbox_to_anchor=(.95,.55))

#right plot
pair_2=['SP500TR','FED']
data_ID_2 = pair_2[0]+'-'+pair_2[1]
print('Figure: fig_final_equity() : '+data_ID_2)

# Read in parameter information for this asset pair
f=open(analysis_folder+'best_fit_parameters.pkl', 'rb')
parameters = pickle.load(f)
f.close()
st_err=parameters[data_ID_2].loc['lopt_error',pair_2[0]]

# Read in optimal leverage values for this asset pair
returns_1=pd.read_pickle(analysis_folder+data_ID_2+"-1.pkl")
returns_2=pd.read_pickle(analysis_folder+data_ID_2+"-2.pkl")
returns_3=pd.read_pickle(analysis_folder+data_ID_2+"-3.pkl")
final_equity_1=np.cumprod(returns_1)[-1:].T
final_equity_2=np.cumprod(returns_2)[-1:].T
final_equity_3=np.cumprod(returns_3)[-1:].T
equity_1=np.cumprod(returns_1)
equity_2=np.cumprod(returns_2)
equity_3=np.cumprod(returns_3)

# Add lines to plot
ax[1].axvline(x=1,linestyle=':',color='red',linewidth=1.5)
ax[1].axvline(x=1+2*st_err,linestyle=':',color='pink',linewidth=1.5)
ax[1].axvline(x=1-2*st_err,linestyle=':',color='pink',linewidth=1.5)
ax[1].axhline(y=0,linestyle=':',color='grey',linewidth=.5)
ax[1].plot(final_equity_1, label='Simple',linewidth=5)
ax[1].plot(final_equity_2, label='+ friction',linewidth=3)
ax[1].plot(final_equity_3, label='+ borrowing premia',linewidth=1)
# Add remaining plot details
# #plt.xlim([final_equity_1.index.min(),final_equity_1.index.max()])
ax[1].set_xlim([-2,6])
ax[1].set_xlabel('leverage')
ax[1].set_ylabel('final equity')
ax[1].legend(loc='best', bbox_to_anchor=(.95,.55))