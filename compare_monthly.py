#!/usr/bin/python
#
# Palmer LTER - Weather Processing Scripts
#
# This script compares two versions of the monthly weather dataset.
# It is currently configured to compare a draft Version 10 datafile with the existing Version 9 file in EDI.
#
# Written by Sage 6/30/23, 5/21/24

import pandas as pd

# Load in the original version 8 dataset
url = 'https://portal.edirepository.org/nis/dataviewer?packageid=knb-lter-pal.189.9&entityid=36ab5972aa4b28481fd24c3bc36c2082'
df1 = pd.read_csv(url, index_col='Date')

# Load in the new version
df2 = pd.read_csv('PalmerStation_Monthly_Weather.csv', index_col='Date')

# Reshape Dataframes to have the same indexes
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
  x1_str = x1.fillna('').map(lambda x: str(x))
  x2_str = x2.fillna('').map(lambda x: str(x))
  xstr = x1_str + ' != ' + x2_str
  return x2.where(x1_str==x2_str,xstr)

df_compare = compare(df1b,df2b)
df_compare = df_compare.replace('nan != nan','')

df_compare.to_csv('diff_monthly_v9_v10.csv')
