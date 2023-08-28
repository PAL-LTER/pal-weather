#!/usr/bin/python
#
# Palmer LTER - Weather Processing Scripts
#
# This script compares two versions of the daily weather dataset.
# It is currently configured to compare the existing Version 8 file in EDI with a draft Version 9.
#
# Written by Sage 6/30/23

import pandas as pd

dtypes = {
  'Precipitation Melted (mm)':str,
  'Precipitation Snow (cm)':str,
  'Depth at Snowstake (cm)':str,
  'Sea Ice (WMO Code)':str}

# Load in the original version 8 dataset
# df1 = pd.read_csv('table_28.csv', index_col='Date', dtype=dtypes)
url = 'https://portal.edirepository.org/nis/dataviewer?packageid=knb-lter-pal.28.8&entityid=375b34051b162d84516ec2d02f864675'
df1 = pd.read_csv(url, index_col='Date', dtype=dtypes)

df1.drop([
  'Data flag - Temperature Average',
  'Data flag - Pressure Average',
  'Wind Peak Direction (True) (º)'], axis=1, inplace=True)
df1.rename(columns={
  'Windspeed Peak':'Wind Peak (knots)',
  'Windspeed 5-Sec Peak':'Wind 5-Sec Peak (knots)',
  'Windspeed 2-Min Peak':'Wind 2-Min Peak (knots)',
  'Windspeed Average':'Wind Average (knots)',
  # 'Wind Peak Direction (True) (º)':'Wind Peak Direction (True)',
  'Wind Peak Direction (º)':'Wind Peak Direction',
  'Wind 5-Sec Peak Direction  (º)':'Wind 5-Sec Peak Direction',
  'Wind 2-Min Peak Direction  (º)':'Wind 2-Min Peak Direction',
  'Wind Direction Prevailing':'Wind Prevailing Direction',
  'Rainfall (mm)':'Precipitation Melted (mm)',
  'Cloud Cover':'Sky Coverage (tenths)'}, inplace=True)

# Load in the new version
df2 = pd.read_csv('PalmerStation_Daily_Weather.csv', index_col='Date', dtype=dtypes)

# Reshape dataframes to have the same indexes
inds = pd.concat([df1,df2]).index.unique().sort_values()
df1b = df1.reindex(inds)
df2b = df2.reindex(inds)

print(df1.shape)
print(df2.shape)
print(df1b.shape)
print(df2b.shape)


# Compare the dataframes and output the results
def compare(x1,x2):
  x1_str = x1.fillna('').applymap(str)
  x2_str = x2.fillna('').applymap(str)
  xstr = x1_str + ' != ' + x2_str
  return x2.where(x1_str==x2_str,xstr)

df_compare = compare(df1b,df2b)
df_compare = df_compare.replace('nan != nan','')

df_compare.to_csv('diff_daily_v8_v9.csv')
