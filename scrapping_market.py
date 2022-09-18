# -*- coding: utf-8 -*-
"""
Created on Thu May 26 18:21:59 2022

@author: ludo_
"""
from pathlib import Path
import pandas as pd
from pandas_datareader import data
def get_tickers(tick_file = "input/cac40_tick.txt"):

    path = Path(tick_file)
    if path.exists() and path.is_file() :
    
        with open(tick_file, "r", encoding="utf8") as data :
        
            for line in data :
                line = line.rstrip()
                tick = line.split(',')
            return tick
    
    else: print(f"No txt file found at {tick_file}. Please provide suitable path.")

def get_values(year):
    # Define the instruments to download.
    tickers = get_tickers()
    
    start_date = str(year)+'-01-01'
    end_date = str(year)+'-12-31'
    
    # User pandas_reader.data.DataReader to load the desired data. As simple as that.
    df = data.DataReader(tickers, 'yahoo', start_date, end_date)
    
    return(df)

def get_sign(row):
   if row['day_dif'] > 0 :
      return True
   if row['day_dif'] < 0 :
       return False
   else :
       return False

def values_cleanup(df):
    
    values_market = {}
    values_df = df
    values_df = values_df.drop(values_df.filter(regex="Adj"), 1)
    #values_df.columns = values_df.columns.droplevel()
    values_df.columns = ['_'.join(col) for col in values_df.columns]
    
    ticks = get_tickers()
    for tick in ticks:
        df_tick = values_df.filter(regex=str(tick))
        df_tick.columns = df_tick.columns.str.replace("_"+str(tick),"")
        values_market[tick] = df_tick
    
    for tick, market in values_market.items():
        market['day_dif'] = market["Close"]-market["Open"]
        market['day_shift'] = market["High"]-market["Low"]
        market['dif_pos'] = market.apply(lambda row: get_sign(row), axis=1)
        
    return values_market