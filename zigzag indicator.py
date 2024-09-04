import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf
from datetime import datetime, timedelta

ticker = "NG=F"
timeframe = 15 #years

#cutoff percentage
zigzag_p = 40

#cutoff multiplier
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

# Defining a temporary high and a dictionary for temporary highs
tmp_high = df["Adj Close"].iloc[0]
tmp_highs_d = {}

# Defining a temporary low and a dictionary for temporary lows
tmp_low = df["Adj Close"].iloc[0]
tmp_lows_d = {}

# Defining the zigzag dataframe for concatination of highs and lows
zigzag_df = pd.DataFrame({"date":df.index[0], "close": [df["Adj Close"].iloc[0]]})

# Iteration trough each row of the yfinance dataframe with price data 
for index, row in df.iterrows():
    # Defining date and close
    date = index
    date_str = date.strftime('%Y-%m-%d')
    close = row["Adj Close"]
    
    # if condition for filling the temporary high dictionary
    if close > tmp_high and close > tmp_low * zph:
            # condition is fulfilled close is now tmp_high
            tmp_high = close
            # new tmp_low threshold for collection of temporary lows
            tmp_low = close * zpl
            # adding new key value pair into tmp_highs_d
            tmp_highs_d[date_str] = tmp_high
            print("highs_d: ", tmp_highs_d)
            
            # make sure tmp_lows_d is not empty
            if not tmp_lows_d:
                print("lows_d is empty")
            # get the lowest value with date from the tmp_lows_d, turn it into a dataframe
            # concat the tl_df df to the zigzag_df
            else:
                lowest_key = min(tmp_lows_d, key=tmp_lows_d.get)
                lowest_value = tmp_lows_d[lowest_key]
                tl_df = pd.DataFrame({"date": [lowest_key], "close": [lowest_value]})
                zigzag_df = pd.concat([zigzag_df, tl_df])
                tmp_lows_d = {}
            
            

    if close < tmp_low and close < tmp_high * zpl: 
            tmp_low = close
            tmp_high = close * zph

            tmp_lows_d[date_str] = tmp_low
            print("lows_d: ", tmp_lows_d)
            
            if not tmp_highs_d:
                print("highs_d is empty")
            else:
                highest_key = max(tmp_highs_d, key=tmp_highs_d.get)
                highest_value = tmp_highs_d[highest_key]
                th_df = pd.DataFrame({"date": [highest_key], "close": [highest_value]})
                zigzag_df = pd.concat([zigzag_df, th_df])
                tmp_highs_d = {}

zigzag_df["date"] = pd.to_datetime(zigzag_df["date"])
zigzag_df = zigzag_df.set_index("date")                       


plt.plot(df.index, df["Adj Close"])
plt.plot(zigzag_df.index, zigzag_df["close"])
plt.show()
    








