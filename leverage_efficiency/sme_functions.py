#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 14:38:01 2018
@author: obp48
"""
import numpy as np
import pandas as pd
import pickle
import scipy.optimize
from lmfit import Model, Parameters
from . import base


def price_to_return(price_series):
    return_series=price_series/price_series.shift(1)
    return_series=return_series[1:]
    return return_series


def get_returns_data(in_file_1, in_file_2, properties):
    #Read in data
    return_series_1=pd.read_pickle(in_file_1)['return']
    return_series_2=pd.read_pickle(in_file_2)['return']

    # We want to keep only dates where both series have a value.
    # We use an inner join to do this neatly
    returns = pd.concat([return_series_1, return_series_2], axis=1, join='inner')
    returns.columns = ['asset 1', 'asset 2']
    rel_ret_1 = returns['asset 1']
    rel_ret_2 = returns['asset 2']

    # Default behaviour is for start and end dates to include entire series
    minimum_start_date = returns.index[0]
    maximum_end_date = returns.index[-1]
    start_date = minimum_start_date
    end_date = maximum_end_date

    # Dafaults can be overwritten if suitable values are provided in properties
    if 'date range' in properties.keys():
        if not properties['date range'][0] == 'min':
            try:
                start_date = pd.to_datetime(properties['date range'][0])
                if start_date < minimum_start_date:
                    print("  Start date supplied is before the start of the time series")
                    raise
            except:
                print("  Failed to override default start date. Reverting to default.\n")
                start_date = minimum_start_date

        if not properties['date range'][1] == 'max':
            try:
                end_date = pd.to_datetime(properties['date range'][1])
                if end_date > maximum_end_date:
                    print("  End date supplied is after the end of the time series")
                    raise
            except:
                print("  Failed to override default end date. Reverting to default.\n")
                end_date = maximum_end_date

    rel_ret_1=rel_ret_1[start_date:end_date]
    rel_ret_2=rel_ret_2[start_date:end_date]

    return start_date, end_date, rel_ret_1, rel_ret_2


def grid(data_folder, analysis_folder, pair):
 print(" ", pair, ": sm.grid()")
 # Extract the individual asset codes from the asset pair
 asset1 = pair.split('-')[0]
 asset2 = pair.split('-')[1]

 # Read market model parameters for the risky asset
 params = base.read_model_parameters()
 long_rate = params[asset1]['long rate']
 short_rate = params[asset1]['short rate']
 friction = params[asset1]['friction']
 leverage_resolution = params[asset1]['leverage resolution']
 eps = params[asset1]['epsilon']

 # Set default properties for this pair (or read them if a file is provided
 # in the modify-defaults folder to over-ride the default properties)
 properties = base.set_pair_properties('modify-defaults/', pair)

 #Read in returns data
 in_file_1=data_folder+asset1+".pkl" #risky
 in_file_2=data_folder+asset2+".pkl" #riskless
 start_date, end_date, rel_ret_1, rel_ret_2 = get_returns_data(in_file_1, in_file_2, properties)
 print("  Using date range "+str(start_date)+ ' - '+str(end_date))

#Set range of leverages avoiding bankruptcy
 min_leverage=-abs(rel_ret_2/(rel_ret_2-rel_ret_1)[rel_ret_2/(rel_ret_2-rel_ret_1)<0]).min()
 max_leverage=abs(rel_ret_2/(rel_ret_2-rel_ret_1)[rel_ret_2/(rel_ret_2-rel_ret_1)>0]).min()

 delta_leverage=max_leverage-min_leverage
 leverage_step_size=delta_leverage/leverage_resolution
 leverage_range=np.arange(min_leverage+eps,max_leverage-eps,leverage_step_size)

#Set up the relative return array (function of time and leverage)
 rel_ret_l=pd.DataFrame(index=rel_ret_1.index,columns=leverage_range)

#Model 1 (simplest case)
 for l in range (0,leverage_range.shape[0]):
     rel_ret_l.iloc[:,l]=model_1(leverage_range[l],rel_ret_1,rel_ret_2)
 rel_ret_l.to_pickle(analysis_folder+pair+'-1.pkl')

#Model 2 with friction
 for l in range (0,leverage_range.shape[0]):
  rel_ret_l.iloc[:,l]=model_2(leverage_range[l],friction,rel_ret_1,rel_ret_2)
#Check if bankruptcy has occurred, declare future returns nan
 rel_ret_l[rel_ret_l<0]=np.nan
 for t in range (1,rel_ret_2.shape[0]):
  rel_ret_l.iloc[t,:]=rel_ret_l.iloc[t,:]+np.where(rel_ret_l.iloc[t-1,:].isna(),np.nan,0)
 rel_ret_l.to_pickle(analysis_folder+pair+'-2.pkl')

#Model 3 with friction and borrowing costs
 for l in range (0,leverage_range.shape[0]):
  rel_ret_l.iloc[:,l]=model_3(leverage_range[l],friction,short_rate,long_rate,rel_ret_1,rel_ret_2)
 #Check if bankruptcy has occurred, declare future returns nan
 rel_ret_l[rel_ret_l<0]=np.nan
 for t in range (1,rel_ret_2.shape[0]):
  rel_ret_l.iloc[t,:]=rel_ret_l.iloc[t,:]+np.where(rel_ret_l.iloc[t-1,:].isna(),np.nan,0)
 rel_ret_l.to_pickle(analysis_folder+pair+'-3.pkl')
 return

#function to fit data: needs to be found
def return_parabola(x, a, xm, b):
    return -a*(x-xm)**2 + b

def print_fit_summary(fit_parameters, pair):
    print(" ",pair," parameter summary:")
    print("    Optimal leverage (model 1) = ", fit_parameters['lopt_1'])
    print("    Optimal leverage (model 2) = ", fit_parameters['lopt_2'])
    print("    Optimal leverage (model 3) = ", fit_parameters['lopt_3'])
    return

def fit_parameters(data_folder, analysis_folder, pair):
 print(" ", pair, ": sm.fit_parameters()")
 # Extract the individual asset codes from the asset pair
 asset1 = pair.split('-')[0]
 asset2 = pair.split('-')[1]

 # Read market model parameters for the risky asset
 params = base.read_model_parameters()

 # Set default properties for this pair (or read them if a file is provided
 # in the modify-defaults folder to over-ride the default properties)
 properties = base.set_pair_properties('modify-defaults/', pair)

 # Read the returns data for both assets
 in_file_1=data_folder+asset1+".pkl" #risky
 in_file_2=data_folder+asset2+".pkl" #riskless
 start_date, end_date, rel_ret_1, rel_ret_2 = get_returns_data(in_file_1, in_file_2, properties)

 print("  Using date range "+str(start_date)+ ' - '+str(end_date))

 Delta_t=end_date-start_date
 years=Delta_t.days/365.25

#Find range of leverages avoiding bankruptcy
 min_leverage=-abs(rel_ret_2/(rel_ret_2-rel_ret_1)[rel_ret_2/(rel_ret_2-rel_ret_1)<0]).min()
 max_leverage=abs(rel_ret_2/(rel_ret_2-rel_ret_1)[rel_ret_2/(rel_ret_2-rel_ret_1)>0]).min()

#find optimal leverages for all models
 lopt_1, eq1 =calculate_optimal_leverage(rel_ret_1,rel_ret_2,[start_date,end_date], 1, params[asset1],bounds=(min_leverage,max_leverage))
 lopt_2, eq2 =calculate_optimal_leverage(rel_ret_1,rel_ret_2,[start_date,end_date], 2, params[asset1],bounds=(min_leverage,max_leverage))
 lopt_3, eq3 =calculate_optimal_leverage(rel_ret_1,rel_ret_2,[start_date,end_date], 3, params[asset1],bounds=(min_leverage,max_leverage))

 lopt_fix=lopt_1
 opt_growth=- eq1/years

 leveraged_returns=pd.read_pickle(analysis_folder+pair+"-1.pkl")
 leveraged_equity=np.cumprod(leveraged_returns)
 final_leveraged_equity=leveraged_equity[-1:].T
 leveraged_growth=np.log(final_leveraged_equity)/years

#create x and y data to be used for curve fitting
 l_input=np.array(leveraged_growth.index[50:-50])
 g_input=np.array(leveraged_growth.iloc[50:-50,0])

 fmodel = Model(return_parabola)
 params = Parameters()
 params.add('a', value=.5, vary=True)
 params.add('xm', value=lopt_fix, vary=False)
 params.add('b', value=opt_growth, vary=False)
 result = fmodel.fit(g_input, params, x=l_input)
 #print(result.fit_report())

 sigma=np.sqrt(2*result.best_values['a'])
 mu_r=opt_growth-(result.best_values['a']*result.best_values['xm']*result.best_values['xm'])
 mu_e=2*result.best_values['a']*result.best_values['xm']


 fit_parameters={'start_date':start_date,
                'years':years,
                'end_date':end_date,
                'min_leverage':min_leverage,
                'max_leverage':max_leverage,
                'sigma_est':sigma,
                'mu_riskless_est':mu_r,
                'mu_excess_est':mu_e,
                'g_riskless_measured':np.log(np.cumprod(rel_ret_2)[-1])/years,
                'g_risky_measured':np.log(np.cumprod(rel_ret_1)[-1])/years,
                'lopt_1':lopt_1,
                'lopt_2':lopt_2,
                'lopt_3':lopt_3,
                'lopt_error':1./(sigma*np.sqrt(years))
                }
 print_fit_summary(fit_parameters, pair)
 return(fit_parameters)


def calculate_optimal_leverage(rel_ret_1,rel_ret_2,time_window,model,model_parameters, bounds=(-500.0,500.0)):
    friction=model_parameters['friction']
    long_rate=model_parameters['long rate']
    short_rate=model_parameters['short rate']

    R1=rel_ret_1[time_window[0]:time_window[1]].values
    R2=rel_ret_2[time_window[0]:time_window[1]].values

    # There are 4 cases based on the properties of the array of differences
    # between the risky and riskless returns in the window
    a = R1 - R2

    if (a == 0.0).all():
        # Optimal leverage is undefined if the returns on the two assets are
        # always equal
        #print(time_window, ' l_opt undefined.')
        return 0.0, 1.0
    elif (a > 0.0).all():
        # Optimal leverage is infinite if the return on the risky asset always
        # exceeds the return on the riskless asset
        #print(time_window, ' l_opt infinite.')
        return np.inf, np.inf
    elif (a < 0.0).all():
        # Optimal leverage is negative infinite if the return on the riskless asset always
        # exceeds the return on the risky asset
        #print(time_window, ' l_opt negative infinite. L = ', (time_window[1]-time_window[0]).days)
        return -np.inf, np.inf
    else:
        # Otherwise optimal leverage is in a bounded interval and should be found
        # by optimising the total equity

        # First find lower and upper bounds. It's OK if we get some divisions
        # by zero since the resulting -np.inf will never be the lower bound
        with np.errstate(divide='ignore'):
            b = -((1.0+R2)/a)

        lower = max(np.where(b<0.0, b, -np.inf))
        upper = min(np.where(b>0.0,b,np.inf))
        # Perform optimisation
        with np.errstate(invalid='ignore', divide='ignore', over='ignore', under='ignore'):
            res = scipy.optimize.minimize_scalar(leveraged_return,  args =(R1,R2,friction, long_rate, short_rate, model),
                bounds=(lower,upper), method='bounded')
        return res.x, res.fun


def leveraged_return(l,rel_ret_1,rel_ret_2,friction, long_rate, short_rate, model):
#Model 1 (simplest case)
    if model==1:
        rel_ret_l=model_1(l,rel_ret_1,rel_ret_2)
#Model 2 with friction
    if model==2:
        rel_ret_l=model_2(l,friction,rel_ret_1,rel_ret_2)
#Model 3 with friction and borrowing costs
    if model==3:
        rel_ret_l=model_3(l,friction,short_rate,long_rate,rel_ret_1,rel_ret_2)
    final_wealth=np.cumprod(rel_ret_l)[-1]

    if final_wealth <= 0.0:
        result = np.inf
    else:
        result = -np.log(final_wealth)
    return result

def model_1(leverage,rel_ret_1,rel_ret_2):
    result = 1.0+leverage*(rel_ret_1-1.0)+(1.0-leverage)*(rel_ret_2-1.0)
    return result

def model_2(leverage,friction,rel_ret_1,rel_ret_2):
    return(1.0+leverage*(rel_ret_1-1.0)+(1.0-leverage)*(rel_ret_2-1.0))\
  -friction*abs(leverage*(1-leverage)*(rel_ret_2-rel_ret_1))

def model_3(leverage,friction,short_rate,long_rate,rel_ret_1,rel_ret_2):
    return((1.0+leverage*(rel_ret_1-1.0)+(1.0-leverage)*(rel_ret_2-1.0))\
  -friction*abs(leverage*(1-leverage)*(rel_ret_2-rel_ret_1))\
  -np.where(leverage<0,abs(leverage),0)*short_rate\
  -np.where(leverage>1,(leverage-1),0)*long_rate)
