# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 20:00:20 2024

@author: fisch
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf
from datetime import datetime, timedelta

ticker = "NG=F"
timeframe = 60 #years
zigzag_p = 40
zph = (100 + zigzag_p) / 100
zpl = (100 - zigzag_p) / 100

# Define the end date as a datetime object
end_date = datetime.strptime("2023-12-31", "%Y-%m-%d")
 #datetime.today() - timedelta(days=)
start_date = end_date - timedelta(days=timeframe*365)

# Format the dates as strings
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")   

# Download the Weekly data
df = yf.download(ticker, start=start_date_str, end=end_date_str, interval='1d')
df.index = pd.to_datetime(df.index)



first_date = df.index[0]
first_date = first_date.strftime('%Y-%m-%d')
first_price = df["Adj Close"].iloc[0]
dic = {first_date : first_price}
tmp_high = df["Adj Close"].iloc[0]
highs = pd.DataFrame({"date":df.index[0], "close": [df["Adj Close"].iloc[0]]})
highs_l = [1]
highs_d = {}
tmp_low = df["Adj Close"].iloc[0]
tmp_startval = df["Adj Close"]
lows = pd.DataFrame({"date":df.index[0], "close": [df["Adj Close"].iloc[0]]})
lows_l = [1]
lows_d = {}
zigzag_df = pd.DataFrame({"date":first_date, "close": [df["Adj Close"].iloc[0]]})
"""
lowest_key = first_date
highest_key = first_date
lowest_value = first_price
highest_value = first_price
"""



for index, row in df.iterrows():
    date = index
    date_str = date.strftime('%Y-%m-%d')
    close = row["Adj Close"]
    
    if close > tmp_high and close > tmp_low * zph:
            tmp_high = close
            tmp_low = close * zpl
            
            highs_d[date_str] = tmp_high
            print("highs_d: ", highs_d)
            
            if not lows_d:
                print("lows_d is empty")
            else:
                lowest_key = min(lows_d, key=lows_d.get)
                lowest_value = lows_d[lowest_key]
                tl_df = pd.DataFrame({"date": [lowest_key], "close": [lowest_value]})
                zigzag_df = pd.concat([zigzag_df, tl_df])
                lows_d = {}
            
            

    if close < tmp_low and close < tmp_high * zpl: 
            tmp_low = close
            tmp_high = close * zph

            lows_d[date_str] = tmp_low
            print("lows_d: ", lows_d)
            
            if not highs_d:
                print("highs_d is empty")
            else:
                highest_key = max(highs_d, key=highs_d.get)
                highest_value = highs_d[highest_key]
                th_df = pd.DataFrame({"date": [highest_key], "close": [highest_value]})
                zigzag_df = pd.concat([zigzag_df, th_df])
                highs_d = {}

zigzag_df["date"] = pd.to_datetime(zigzag_df["date"])
zigzag_df = zigzag_df.set_index("date")                       

df["Adj Close"].plot()            
zigzag_df.plot()

print(zigzag_df)
plt.show()

plt.plot(df.index, df["Adj Close"])
plt.plot(zigzag_df.index, zigzag_df["close"])
plt.show()
    
"""    
    if close > highs["close"].iloc[-1]:
        if close > (tmp_high * ((100 + zigzag_p)/100)):
            tmp_high = close
            
            highs_con = pd.DataFrame({"date":date,"close":close})
            highs=pd.concat([highs,highs_con])
            tmp_low = tmp_high
            print(tmp_high)
    
    if close < lows["close"].iloc[-1]:       
        if close < (tmp_low * ((100 + zigzag_p)/100)):
            tmp_low = close
            tmp_high = tmp_low
            lows_con = pd.DataFrame({"date":date,"close":close})
            lows=pd.concat([lows,lows_con])
            print(tmp_low)
        

    #print("Index: ", date, " and Row: ", row)
"""    












