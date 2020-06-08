import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
from datetime import datetime

def standard_plot(dataframe, columns, labels, ratio=1.0):
    # Create figure and axes objects for plotting to
    fig=plt.figure()
    ax = plt.axes()

    # Add the specified columns from the dataframe to the plot
    for tag in columns:
        label =  labels[tag]
        dataframe[tag].plot(label=label, ax=ax)

    # Set some plot features
    plt.legend(loc='upper right', ncol=1, mode="expand", framealpha=1.0)

    # Return the figure and axis objects for subsequent tweaking
    return fig, ax

def fig_exp_window(analysis_folder, pair):
    print('Figure: fig_exp_window() : '+pair)

    # Read in optimal leverage values for this asset pair
    lopt_1=pd.read_pickle(analysis_folder+pair+"-1_lopt_exp.pkl")
    lopt_2=pd.read_pickle(analysis_folder+pair+"-2_lopt_exp.pkl")
    lopt_3=pd.read_pickle(analysis_folder+pair+"-3_lopt_exp.pkl")

    # Read in parameter information for this asset pair
    filename = analysis_folder+pair+'_prm.pkl'
    f=open(filename, 'rb')
    parameters = pickle.load(f)[pair]
    f.close()
    sigma=parameters['sigma_est']
    l_max=parameters['max_leverage']
    l_min=parameters['min_leverage']

    # Create plot
    fig=plt.figure()
    ax = plt.axes()
    # Add data lines
    plt.plot(lopt_1.index,1+1./np.sqrt(sigma*sigma*(lopt_1.index-lopt_1.index[0]).days/365.25),color='pink',linestyle='--')
    plt.plot(lopt_1.index,1-1./np.sqrt(sigma*sigma*(lopt_1.index-lopt_1.index[0]).days/365.25),color='pink',linestyle='--')
    plt.plot(lopt_1.index,1+2./np.sqrt(sigma*sigma*(lopt_1.index-lopt_1.index[0]).days/365.25),color='pink',linestyle=':')
    plt.plot(lopt_1.index,1-2./np.sqrt(sigma*sigma*(lopt_1.index-lopt_1.index[0]).days/365.25),color='pink',linestyle=':')
    plt.plot(lopt_1, label='simple')
    plt.plot(lopt_2, label='+ friction')
    plt.plot(lopt_3, label='+ borrowing premia')
    plt.plot(lopt_1, label='',color='C0')
    # Add remaining plot details
    plt.xlabel('end date')
    plt.ylabel('optimal leverage')
    plt.axhline(y=1,linestyle=':',color='grey',linewidth=.5)
    plt.axhline(y=0,linestyle=':',color='grey',linewidth=.5)
    plt.legend(loc='best')
    plt.xlim([lopt_1.index[0],lopt_1.index[-1]])
    plt.ylim([1.5*l_min,1.5*l_max])
    return fig, ax


def fig_compare_assets(analysis_folder, plots_folder):
    print('Figure: fig_compare_assets() : ')
    # Read in returns
    returns_1=pd.read_pickle(analysis_folder+"MAD-FEDM-1.pkl")
    returns_2=pd.read_pickle(analysis_folder+"SP500-FED-1.pkl")
    # returns_3=pd.read_pickle(analysis_folder+"DAX-IRDE-1.pkl")
    returns_4=pd.read_pickle(analysis_folder+"BTC-FED-1.pkl")
    returns_5=pd.read_pickle(analysis_folder+"BRK-FED-1.pkl")
    final_equity_1=np.cumprod(returns_1)[-1:].T
    final_equity_2=np.cumprod(returns_2)[-1:].T
    # final_equity_3=np.cumprod(returns_3)[-1:].T
    final_equity_4=np.cumprod(returns_4)[-1:].T
    final_equity_5=np.cumprod(returns_5)[-1:].T
#
    filename = analysis_folder+'MAD-FEDM_prm.pkl'
    f=open(filename, 'rb')
    parameters = pickle.load(f)['MAD-FEDM']
    f.close()
    years_1=parameters['years']

    filename = analysis_folder+'SP500-FED_prm.pkl'
    f=open(filename, 'rb')
    parameters = pickle.load(f)['SP500-FED']
    f.close()
    years_2=parameters['years']

    # filename = analysis_folder+'DAX-IRDE_prm.pkl'
    # f=open(filename, 'rb')
    # parameters = pickle.load(f)['DAX-IRDE']
    # f.close()
    # years_3=parameters['years']

    filename = analysis_folder+'BTC-FED_prm.pkl'
    f=open(filename, 'rb')
    parameters = pickle.load(f)['BTC-FED']
    f.close()
    years_4=parameters['years']

    filename = analysis_folder+'BRK-FED_prm.pkl'
    f=open(filename, 'rb')
    parameters = pickle.load(f)['BRK-FED']
    f.close()
    years_5=parameters['years']

    # Create plot
    fig=plt.figure()
    ax = plt.axes()
    # Add lines to plot
    plt.axvline(x=1,linestyle=':',color='red',linewidth=.5)
    plt.axhline(y=0,linestyle=':',color='grey',linewidth=.5)
    plt.plot(np.log(final_equity_1)/years_1,label='Madoff',linewidth=2,color='green')
    plt.plot(np.log(final_equity_5)/years_5,label='Berkshire Hathaway',linewidth=2,color='orange')
    plt.plot(np.log(final_equity_2)/years_2,label='S&P500',linewidth=2,color='blue')
    # plt.plot(np.log(final_equity_3)/years_3,label='DAX',linewidth=2,color='magenta')
    plt.plot(np.log(final_equity_4)/years_4,label='Bitcoin',linewidth=2,color='red')
    # Add remaining plot details
    plt.xlim([-35,110])
    plt.ylim([-4,5])
    #plt.xlim([final_equity_1.index.min(),final_equity_1.index.max()])
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:3.0f}% p.a.'.format(100*x) for x in vals])
    plt.xlabel('leverage')
    plt.ylabel('growth rate')
    plt.legend(loc='best')
    return fig, ax

def fig_growth_vs_leverage(analysis_folder, plots_folder, pair):
    print('Figure: fig_growth_vs_leverage() : '+pair)
    # Read in optimal leverage values for this asset pair
    returns_1=pd.read_pickle(analysis_folder+pair+"-1.pkl")
    returns_2=pd.read_pickle(analysis_folder+pair+"-2.pkl")
    returns_3=pd.read_pickle(analysis_folder+pair+"-3.pkl")
    final_equity_1=np.cumprod(returns_1)[-1:].T
    final_equity_2=np.cumprod(returns_2)[-1:].T
    final_equity_3=np.cumprod(returns_3)[-1:].T
    equity_1=np.cumprod(returns_1)
    equity_2=np.cumprod(returns_2)
    equity_3=np.cumprod(returns_3)
    #
    # Read in parameter information for this asset pair
    filename = analysis_folder+pair+'_prm.pkl'
    f=open(filename, 'rb')
    parameters = pickle.load(f)[pair]
    f.close()
    years=parameters['years']
    sigma=parameters['sigma_est']
    mu_e=parameters['mu_excess_est']
    mu_r=parameters['mu_riskless_est']
    lopt_est=parameters['lopt_1']
    st_err=parameters['lopt_error']

    # Create plot
    fig=plt.figure()
    ax = plt.axes()
    # Add lines to plot
    plt.axvline(x=lopt_est,linestyle='--',color='black',linewidth=1.5)
    plt.axvline(x=1,linestyle=':',color='red',linewidth=1.5)
    plt.axvline(x=1+2*st_err,linestyle=':',color='pink',linewidth=1.5)
    plt.axvline(x=1-2*st_err,linestyle=':',color='pink',linewidth=1.5)
    plt.axhline(y=0,linestyle=':',color='grey',linewidth=.5)
    (np.log(final_equity_1.iloc[:,0].astype(float))/years).plot(label='simple', linewidth=5, color='blue')
    (np.log(final_equity_2.iloc[:,0].astype(float))/years).plot(label='+ friction', linewidth=3, color='orange')
    (np.log(final_equity_3.iloc[:,0].astype(float))/years).plot(label='+ borrowing premia', linewidth=1, color='green')
    plt.plot(final_equity_1.index,\
              (mu_r+mu_e*final_equity_1.index-sigma**2*final_equity_1.index**2/2),\
              linestyle="--",linewidth=4, color='red')
    # Add remaining plot details
    plt.xlim([-6.5,8.5])
    #plt.xlim([final_equity_1.index.min(),final_equity_1.index.max()])
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:3.0f}% p.a.'.format(100*x) for x in vals])
    plt.xlabel('leverage')
    plt.ylabel('growth rate')
    plt.legend(loc='best')
    return fig, ax

def fig_growth_vs_leverage_all(analysis_folder, plots_folder):
    input_dir=analysis_folder
    returns_1=pd.read_pickle(input_dir+"SP500-FED-1.pkl")
    returns_2=pd.read_pickle(input_dir+"BRK-FED-1.pkl")
    returns_3=pd.read_pickle(input_dir+"BTC-FED-1.pkl")
    final_equity_1=np.cumprod(returns_1)[-1:].T
    final_equity_2=np.cumprod(returns_2)[-1:].T
    final_equity_3=np.cumprod(returns_3)[-1:].T

    f=open(analysis_folder+'SP500-FED_prm.pkl', 'rb')
    parameters = pickle.load(f)
    lopt_error_1=parameters['SP500-FED']['lopt_error']
    f.close()

    f=open(analysis_folder+'BRK-FED_prm.pkl', 'rb')
    parameters = pickle.load(f)
    lopt_error_2=parameters['BRK-FED']['lopt_error']
    f.close()

    f=open(analysis_folder+'BTC-FED_prm.pkl', 'rb')
    parameters = pickle.load(f)
    lopt_error_3=parameters['BTC-FED']['lopt_error']
    f.close()

    ####final equity vs. leverage#####
    fig, ax1=plt.subplots()
    plt.axvline(x=1,linestyle=':',color='black',linewidth=1.5)
    ax1.fill_betweenx([.01,10**6],1+2*lopt_error_3, 1-2*lopt_error_3,color=(1,0,0,0.3))
    ax1.fill_betweenx([.01,10**6],1+2*lopt_error_3, 1+2*lopt_error_2,color=(1,1,0,0.2))
    ax1.fill_betweenx([.01,10**6],1-2*lopt_error_3, 1-2*lopt_error_2,color=(1,1,0,0.2))
    ax1.fill_betweenx([.01,10**6],1+2*lopt_error_2, 1+2*lopt_error_1,color=(0,0,1,0.2))
    ax1.fill_betweenx([.01,10**6],1-2*lopt_error_2, 1-2*lopt_error_1,color=(0,0,1,0.2))
    plt.axvline(x=1+2*lopt_error_3,linestyle=':',color='red',linewidth=.5)
    plt.axvline(x=1-2*lopt_error_3,linestyle=':',color='red',linewidth=.5)
    plt.axvline(x=1+2*lopt_error_1,linestyle=':',color='blue',linewidth=.5)
    plt.axvline(x=1-2*lopt_error_1,linestyle=':',color='blue',linewidth=.5)
    plt.axvline(x=1+2*lopt_error_2,linestyle=':',color='orange',linewidth=.5)
    plt.axvline(x=1-2*lopt_error_2,linestyle=':',color='orange',linewidth=.5)
    plt.axhline(y=0,linestyle=':',color='grey',linewidth=.5)
    ax1.plot(final_equity_1, label='S&P500',linewidth=2,color='blue')
    ax1.plot(final_equity_2, label='Berkshire',linewidth=2,color='orange')
    ax1.plot(final_equity_3, label='Bitcoin',linewidth=2,color='red')
    ax1.set_yscale('log')
    ax1.set_xlim([-2,6])
    ax1.set_ylim([0.01,10**6])
    ax1.set_xlabel('leverage')
    ax1.set_ylabel('final equity')

    ax1.legend(loc='best')
    return fig, ax1



def fig_final_equity(analysis_folder, plots_folder, pair):
    print('Figure: fig_final_equity() : '+pair)

    # Read in parameter information for this asset pair
    filename = analysis_folder+pair+'_prm.pkl'
    f=open(filename, 'rb')
    parameters = pickle.load(f)[pair]
    f.close()
    st_err=parameters['lopt_error']

    # Read in optimal leverage values for this asset pair
    returns_1=pd.read_pickle(analysis_folder+pair+"-1.pkl")
    # returns_2=pd.read_pickle(analysis_folder+pair+"-2.pkl")
    # returns_3=pd.read_pickle(analysis_folder+pair+"-3.pkl")
    final_equity_1=np.cumprod(returns_1)[-1:].T
    # final_equity_2=np.cumprod(returns_2)[-1:].T
    # final_equity_3=np.cumprod(returns_3)[-1:].T
    equity_1=np.cumprod(returns_1)
    # equity_2=np.cumprod(returns_2)
    # equity_3=np.cumprod(returns_3)

    # Create plot
    fig=plt.figure()
    ax = plt.axes()
    # Add lines to plot
    plt.axvline(x=1,linestyle=':',color='red',linewidth=1.5)
    plt.axvline(x=1+2*st_err,linestyle=':',color='pink',linewidth=1.5)
    plt.axvline(x=1-2*st_err,linestyle=':',color='pink',linewidth=1.5)
    plt.axhline(y=0,linestyle=':',color='grey',linewidth=.5)
    plt.plot(final_equity_1, label='',linewidth=2)
    # plt.plot(final_equity_2, label='+ friction',linewidth=3)
    # plt.plot(final_equity_3, label='+ borrowing premia',linewidth=1)
    # Add remaining plot details
    # #plt.xlim([final_equity_1.index.min(),final_equity_1.index.max()])
    if pair=='SP500-FED':
        ax.plot(final_equity_1.index[277],final_equity_1.iloc[277],marker='o',markerfacecolor='none',linewidth=.1,color='C0')
        ax.plot(final_equity_1.index[299],final_equity_1.iloc[299],marker='o',markerfacecolor='none',linewidth=.1,color='C1')
        ax.plot(final_equity_1.index[320],final_equity_1.iloc[320],marker='o',markerfacecolor='none',linewidth=.1,color='C2')
        ax.plot(final_equity_1.index[344],final_equity_1.iloc[344],marker='o',markerfacecolor='none',linewidth=.1,color='C3')
        ax.plot(final_equity_1.index[366],final_equity_1.iloc[366],marker='o',markerfacecolor='none',linewidth=.1,color='C4')
        ax.plot(final_equity_1.index[390],final_equity_1.iloc[390],marker='o',markerfacecolor='none',linewidth=.1,color='C5')

        ax.annotate('l=0',
            xy=(0,final_equity_1.iloc[277]), xycoords='data',
            xytext=(-60, 0), textcoords='offset points',
            arrowprops=dict(color='C0',arrowstyle="->"))
        ax.annotate('l=0.5',
            xy=(0.5,final_equity_1.iloc[299]), xycoords='data',
            xytext=(-60, 0), textcoords='offset points',
            arrowprops=dict(color='C1',arrowstyle="->"))
        ax.annotate('l=1',
            xy=(1,final_equity_1.iloc[320]), xycoords='data',
            xytext=(-60, 0), textcoords='offset points',
            arrowprops=dict(color='C2',arrowstyle="->"))
        ax.annotate('l=1.5',
            xy=(1.5,final_equity_1.iloc[344]), xycoords='data',
            xytext=(50, 0), textcoords='offset points',
            arrowprops=dict(color='C3',arrowstyle="->"))
        ax.annotate('l=2',
            xy=(2,final_equity_1.iloc[366]), xycoords='data',
            xytext=(50, 0), textcoords='offset points',
            arrowprops=dict(color='C4',arrowstyle="->"))
        ax.annotate('l=2.5',
            xy=(2.5,final_equity_1.iloc[390]), xycoords='data',
            xytext=(50, 0), textcoords='offset points',
            arrowprops=dict(color='C5',arrowstyle="->"))
    plt.xlim([-2,4])
    plt.xlabel('leverage')
    plt.ylabel('final equity')
    plt.legend(loc='best')
    return fig, ax

def fig_equity_trajectories(analysis_folder, plots_folder, pair):
    print('Figure: fig_equity_trajectories() : '+pair)
    # Read in equity data
    returns=pd.read_pickle(analysis_folder+pair+'-1.pkl')
    equity=np.cumprod(returns)
    final_equity=equity[-1:].T
    #
    # #### equity trajectories ####
    fig=plt.figure()
    ax = plt.axes()
    # Add lines to plot
    Delta_t=returns.index[-1] - returns.index[0]
    years=Delta_t.days/365.25
#    equity.iloc[:,99].plot(label='l='+str(round(equity.columns[99],2)))
    equity.iloc[:,277].plot(label='l='+str(round(equity.columns[277],1)))
    equity.iloc[:,299].plot(label='l='+str(round(equity.columns[299],1)))
    equity.iloc[:,320].plot(label='l='+str(round(equity.columns[320],1)))
    equity.iloc[:,344].plot(label='l='+str(round(equity.columns[344],1)))
    equity.iloc[:,366].plot(label='l='+str(round(equity.columns[366],1)))
    equity.iloc[:,390].plot(label='l='+str(round(equity.columns[390],1)))
    # Add remaining plot details
    if pair=='SP500-FED':
        # plt.annotate(r'l=0',(equity.index[-1],equity.iloc[-1,277]))
        plt.annotate(r'l=0',(1.02,.183),xycoords='axes fraction')
        # plt.annotate(r'l=0.5',(equity.index[-1],equity.iloc[-1,299]))
        plt.annotate(r'l=0.5',(1.02,.53),xycoords='axes fraction')
        # plt.annotate(r'l=1',(equity.index[-1],equity.iloc[-1,320]))
        plt.annotate(r'l=1',(1.02,.845),xycoords='axes fraction')
        # plt.annotate(r'l=1.5',(equity.index[-1],equity.iloc[-1,344]))
        plt.annotate(r'l=1.5',(1.02,.655),xycoords='axes fraction')
        # plt.annotate(r'l=2',(equity.index[-1],equity.iloc[-1,366]))
        plt.annotate(r'l=2',(1.02,.26),xycoords='axes fraction')
        # plt.annotate(r'l=2.5',(equity.index[-1],equity.iloc[-1,390]))
        plt.annotate(r'l=2.5',(1.02,.073),xycoords='axes fraction')
#    ax.set_yscale('log')
    plt.xlabel('')
    plt.ylabel('equity')
    plt.legend(loc='best')

    return fig, ax

def fig_lopt_var(analysis_folder, plots_folder, pairs):
    #data_ID = pair[0]+'-'+pair[1]
    print('Figure: fig_lopt_var()')

    sigma={}
    lopt_var={}
    for pair in pairs:
        # Read in parameter information for this asset pair
        filename = analysis_folder+pair+'_prm.pkl'
        f=open(filename, 'rb')
        parameters = pickle.load(f)[pair]
        f.close()
        sigma[pair]=parameters['sigma_est']

        # Read in leverage data
        lopt_var[pair]=pd.read_pickle(analysis_folder+pair+"_lopt_var.pkl")

    # Create plot
    fig=plt.figure()
    ax = plt.axes()
    # Add lines to plot
    ci=0
    for pair in pairs:
        col='C'+str(ci)
        #plt.loglog(lopt_var.index.days,(lopt_var.index.days/365.25)**-0.5/sigma,linestyle='--')
        #plt.loglog(lopt_var.index.days,np.sqrt(lopt_var),color='red',marker='o',linestyle='', label=pair[0])
        plt.loglog(lopt_var[pair].index.days,(lopt_var[pair].index.days/365.25)**-0.5/sigma[pair],linestyle='--',color=col)
        plt.loglog(lopt_var[pair].index.days,np.sqrt(lopt_var[pair]),marker='o',linestyle='', label=pair,color=col)
        ci=ci+1

    # Add remaining plot details
    plt.xlabel('window size')
    plt.ylabel('Standard deviation of optimal leverage')
    plt.xlim([10,10000])
    plt.ylim([.1,1000])
    plt.legend(loc='best')
    return fig, ax

def fig_leverage_vary_window(analysis_folder, plots_folder, pair, model):
    print('Figure: fig_leverage_vary_window() : '+pair)
    # Read in optimal leverage data for different window lengths
    df=pd.read_pickle(analysis_folder+pair+'-'+str(model)+'_lopt_fixed.pkl')
    #
    # Create plot
    fig=plt.figure()
    ax = plt.axes()
    # Add lines to plot
    if pair=='SP500-FED':
        for c in df.columns[1:]:
            label = str(int(c/365))+ ' year'
            df[c].plot(label=label)
    else:
        for c in df.columns:
            label = str(int(c/365))+ ' year'
            df[c].plot(label=label)

    plt.axhline(y=0,linestyle='-',color='black',linewidth=.5)
    plt.axhline(y=1,linestyle=':',color='black',linewidth=1.0)
    # Add remaining plot details
    plt.xlabel('window end date')
    plt.ylabel('optimal leverage')
    plt.legend(loc='best')
    ymax = min(1.5*df[365].max(), 50.0)
    ymin = max(1.5*df[365].min(), -50.0)
    plt.ylim([ymin, ymax])

    return fig, ax
