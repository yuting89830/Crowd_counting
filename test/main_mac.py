# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime
from statsmodels.tsa.arima.model import ARIMA
import pytz

# Read MAC address data from CSV file
def read_mac_addresses_from_csv():
    try:
        df = pd.read_csv('lib_log_0727.csv')  # Set the path for the CSV file
        return df
    except FileNotFoundError as e:
        print("CSV file not found:", e)
        return None

# Use ARIMA model for forecasting
def arima_forecast(data, order=(1, 1, 1)):
    try:
        model = ARIMA(data, order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=1)
        if forecast:
            return forecast[0]
        else:
            print("The ARIMA model did not predict successfully.")
            return None
    except Exception as e:
        print("An error occurred in the ARIMA model:", e)
        return None

# Main function
def main():
    # Read MAC address data from CSV file
    df = read_mac_addresses_from_csv()
    if df is None:
        return

    # Count the number of MAC address changes every five minutes 
    df['TID'] = pd.to_datetime(df['TID'], unit='s')  
    df.set_index('TID', inplace=True) 
    taipei_tz = pytz.timezone('Asia/Taipei')
    df.index = df.index.tz_localize(pytz.utc).tz_convert(taipei_tz)
    df_resampled = df.resample('5T').apply(lambda x: len(x['MAC'].unique())) 
    df_resampled.fillna(0, inplace=True) 
    
    print("Number of MAC address changes every five minutes:")
    for index, value in df_resampled.items():
        print(index, value)

    # Into new csv
    df_resampled.to_csv('MAC_change.csv', header=['MAC_change'])

    # Count the current number of MAC addresses
    num_mac_addresses = len(df)
    print("There are {} MAC addresses at present.".format(num_mac_addresses))

    # Perform ARIMA forecasting
    data = df["MAC"].value_counts().tolist()
    forecast_value = arima_forecast(data)
    if forecast_value is not None:
        print("Forecasted number of people at a future time point:", forecast_value)
    else:
        print("The prediction of the number of people at a certain point in the future fails.")
    

if __name__ == "__main__":
    main()
