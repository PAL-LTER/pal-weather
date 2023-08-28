#!/usr/bin/python
#
# Script to compare new Version 9 datafile with the existing Version 8 file in EDI.
# Written by Sage 6/30/23

import pandas as pd

dtypes = {
  'Precipitation Melted (mm)':str,
  'Precipitation Snow (cm)':str,
  'Depth at Snowstake (cm)':str,
  'Sea Ice (WMO Code)':str}

# Load in the original version 8 dataset
# df1 = pd.read_csv('table_189.csv', index_col='Date', dtype=dtypes)
url = 'https://portal.edirepository.org/nis/dataviewer?packageid=knb-lter-pal.189.8&entityid=ab357b4c92531a07d98ff1c4f4809a1e'
df1 = pd.read_csv(url, index_col='Date', dtype=dtypes)

df1.drop(['Year','Month'], axis=1, inplace=True)
df1.rename(columns={
  'Average Temperature (C)':'Mean Temperature (C)',
  'Average Pressure (mbar)':'Mean Pressure (mbar)',
  'Average Melted Precipitation (mm)':'Mean Precipitation (mm)',
  'Temperature  Count':'Temperature Count'
}, inplace=True)

# Load in the new version
df2 = pd.read_csv('PalmerStation_Monthly_Weather.csv', index_col='Date', dtype=dtypes)
df2.drop(['Sum Precipitation (mm)',
  'Mean Sea Surface Temperature (C)', 'Sea Surface Temperature Count',
  'Mean Windspeed (knots)', 'Windspeed Count'], axis=1, inplace=True)

# Reshape dataframes to have the same indexes
inds = pd.concat([df1,df2]).index.unique().sort_values()
df1b = df1.reindex(inds)
df2b = df2.reindex(inds)

print(df1.dtypes)
print(df2.dtypes)
print(df1.shape)
print(df2.shape)
print(df1b.shape)
print(df2b.shape)

# Compare the 2 DataFrames and output the results
def compare(x1,x2):
  x1_str = x1.fillna('').applymap(str)
  x2_str = x2.fillna('').applymap(str)
  xstr = x1_str + ' != ' + x2_str
  return x2.where(x1_str==x2_str,xstr)

df_compare = compare(df1b,df2b)
df_compare = df_compare.replace('nan != nan','')

df_compare.to_csv('diff_monthly_v8_v9.csv')
