#!/usr/bin/python
#
# Palmer LTER - Weather Processing Scripts
#
# This script calculates the monthly average weather data for Palmer Station.
# The original daily  were obtained from the UW-Madison ARMC archive and merged using
#
# Written by Sage 7/10/23

import argparse
import pandas as pd
import numpy as np

# Primary function
def main():
  df = pd.read_csv('PalmerStation_Daily_Weather.csv', index_col='Date', parse_dates=True)
  
  # Fix Precipitation - Version 8 considered Trace to be NaN.  In version 9, let's make them 0.
  df['Precipitation Melted (mm)'].replace('T', 0, inplace=True)  # Change to np.nan if desired
  df['Precipitation Melted (mm)'] = df['Precipitation Melted (mm)'].astype('float64')
  
  # Fill in simplistic averages of temp and pressure
  df['Temperature Average (C)'].fillna( (df['Temperature High (C)'] + df['Temperature Low (C)'])/2, inplace=True)
  df['Pressure Average (mbar)'].fillna( (df['Pressure High (mbar)'] + df['Pressure Low (mbar)'])/2, inplace=True)
  
  # Remove low pressure values
  df['Pressure Average (mbar)'].where(df['Pressure Average (mbar)']>800, inplace=True)
  
  df_avg = df.resample('1MS').agg({
    'Temperature Average (C)' : ['mean', 'count'],
    'Pressure Average (mbar)' : ['mean', 'count'],
    'Precipitation Melted (mm)' : ['mean', 'sum', 'count'],
    'Sea Surface Temperature (C)' : ['mean', 'count'],
    'Wind Average (knots)' : ['mean', 'count'],
  })
  
  # Add old temps from Baker 1996
  df0 = pd.read_csv('monthly_temps_1974_1989.csv', index_col='Date', parse_dates=True)
  df0.drop(['Year','Month'], axis=1, inplace=True)
  df0.columns = pd.MultiIndex.from_tuples([("Temperature Average (C)", "mean")])
  df_avg = pd.concat([df0, df_avg])
  print(df_avg)
  
  # Save to CSV
  df_avg.to_csv(args.fname, float_format='%2.2f', header=[
    'Mean Temperature (C)','Temperature Count',
    'Mean Pressure (mbar)','Pressure Count',
    'Mean Precipitation (mm)','Sum Precipitation (mm)','Precipitation Count',
    'Mean Sea Surface Temperature (C)', 'Sea Surface Temperature Count',
    'Mean Windspeed (knots)', 'Windspeed Count'])
  print('Output file: %s' %args.fname)


# Main function for command line mode
if __name__ == '__main__':
  # Command Line Arguments
  parser = argparse.ArgumentParser(description='PAL Monthly Climatology')
  parser.add_argument('-f','--fname', type=str,
    default='PalmerStation_Monthly_Weather.csv',
    help='Output filename')
  args = parser.parse_args()
  main()
