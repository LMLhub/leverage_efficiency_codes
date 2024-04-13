import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import leverage_efficiency.base
import leverage_efficiency.data as data
import yaml
import sys

def main(config_file):
    # Read the config information to control what gets executed
    f = open(config_file,'r')
    config = yaml.load(f, Loader=yaml.SafeLoader)
    f.close()

    # Download latest data into a dataframe
#    tickers = ['^SP500TR', '^GDAXI', 'BTC-USD']
    tickers = ['^SP500TR', '^GDAXI', 'BTC-USD']
    df1 = data.download_yahoo(tickers)

#    data_url ='http://www.cryptodatadownload.com/cdd/Kraken_BTCUSD_d.csv'
#    df2 = data.download_csv(data_url, ['Date','Close'], ['Date','Level'], header=1)
    #print(df2.head())

#    data_url ='http://lml.org.uk/wp-content/uploads/2019/12/madoff.csv'
#    df3 = data.download_csv(data_url,['month','monthly percentage return'], ['Date','Return'])
    #print(df3.head())

    data_url ='http://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=FEDFUNDS&scale=left&cosd=1954-07-01&coed=2020-03-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2009-06-01&line_index=1&transformation=lin&vintage_date=2020-04-29&revision_date=2020-04-29&nd=1954-07-01'
    df4 = data.download_csv(data_url,['DATE','FEDFUNDS'], ['Date','Level'])

    #print(df4.head())


# Execute the main() function

if __name__ == "__main__":
    # Get the name of the config file
    config_file = leverage_efficiency.base.get_config_filename(sys.argv)
    main(config_file)
