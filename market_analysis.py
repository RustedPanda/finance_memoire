# -*- coding: utf-8 -*-
"""
Created on Sun May 29 10:21:23 2022

@author: ludo_
"""

import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from dateutil.parser import parse
from sklearn import linear_model

pd.set_option('display.max_columns', 500)

def add_freq(idx, freq=None):
    """Add a frequency attribute to idx, through inference or directly.

    Returns a copy.  If `freq` is None, it is inferred.
    """

    idx = idx.copy()
    if freq is None:
        if idx.freq is None:
            freq = pd.infer_freq(idx)
        else:
            return idx
    idx.freq = pd.tseries.frequencies.to_offset(freq)
    if idx.freq is None:
        raise AttributeError('no discernible frequency found to `idx`.  Specify'
                             ' a frequency string with `freq`.')
    return idx

def correlation(sentiments,market,year):
    
    for (filename,sents), (tick,values) in zip(sentiments.items(), market.items()):

        list_corr1 = []
        list_corr2 = []
        list_corr3 = []
        list_corr4 = []

        values_f = values.dropna()
        sents.index = sents.index.tz_localize(None)
        values.index = values.index.tz_localize(None)

        full = (pd.merge(sents, values, on = "Date", how="inner")).dropna()

        new_index = pd.date_range(start=str(year)+'-01-01', end=str(
            year)+'-12-31', freq='D', tz= None)

        #values.index = new_index
        for n in range(1,13) :
            month =  full[full.index.month == n]

            reg = linear_model.LinearRegression()
            reg.fit(month.index.values.reshape(-1, 1), month['Close'].values)

            if reg.coef_ > 0 :

            else :


        # for val in values:
        #     ts1 = values[str(val)]
        #     ts2 = sents["Score"]
        #     ts3 = sents["Score_blob"]
        #     ts4 = sents["Vader_cat"]
        #     ts5 = sents["Blob_cat"]
        #     corr = ts1.corr(ts2)
        #     corr2 = ts1.corr(ts3)
        #     corr3 = ts1.corr(ts4)
        #     corr4 = ts1.corr(ts5)
        #     list_corr1.append(corr)
        #     list_corr2.append(corr2)
        #     list_corr3.append(corr3)
        #     list_corr4.append(corr4)
        #     print(f"Correlation score between {filename[:-8]} market variable "
        #           f"'{str(val)}' and Vader twitter sentiments is :\n{corr}")
        #     print(f"Correlation score between {filename[:-8]} market variable "
        #           f"'{str(val)}' and Blob twitter sentiments is :\n{corr2}\n")
        #     print(f"Correlation score between {filename[:-8]} market variable "
        #           f"'{str(val)}' and Vader sentiments' category is :\n{corr3}")
        #     print(f"Correlation score between {filename[:-8]} market variable "
        #           f"'{str(val)}' and Blob sentiments's category is :\n{corr4}")