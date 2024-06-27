#!/usr/bin/python
#
# Palmer LTER - Weather Processing Scripts
# Daily averaged weather: knb-lter-pal.28
#
# This script merges the daily weather (climatology) data files from the UW-Madison ARMC archive.
# It combines a hand-edited set of files from 1989 to 2017-02 (found in the
# climatology_cleaned directory), with a set of files from 2017-03 onward (found
# in the in climatology directory) that were recently updated by the Palmer RA
# to be more consistent in format, and to fix a number of export processing issues.
#
# Edited by Sage Lichtenwalner, Rutgers University, 8/18/2023, 5/21/2024

import argparse
import pandas as pd
import io
import glob

# Define Dataset Headers
head_198904 = ['Day','Temperature High (C)','Temperature Low (C)','Temperature Average (C)',
               'Pressure High (mbar)','Pressure Low (mbar)','Pressure Average (mbar)',
               'Wind Peak (knots)','Wind Peak Direction',
               'Wind Average (knots)','Wind Prevailing Direction',
               'Precipitation Melted (mm)','Precipitation Snow (cm)','Depth at Snowstake (cm)',
               'Sky Coverage (tenths)','Sea Temp/Ice'];
head_200310 = ['Day','Temperature High (C)','Temperature Low (C)','Temperature Average (C)',
               'Pressure High (mbar)','Pressure Low (mbar)','Pressure Average (mbar)',
               'Wind 5-Sec Peak (knots)','Wind 2-Min Peak (knots)','Wind 2-Min Peak Direction',
               'Wind Average (knots)','Wind Prevailing Direction',
               'Precipitation Melted (mm)','Precipitation Snow (cm)','Depth at Snowstake (cm)',
               'Sky Coverage (tenths)','Sea Temp/Ice'];
head_200405 = ['Day','Temperature High (C)','Temperature Low (C)','Temperature Average (C)',
               'Pressure High (mbar)','Pressure Low (mbar)','Pressure Average (mbar)',
               'Wind 5-Sec Peak (knots)','Wind 2-Min Peak (knots)','Wind 2-Min Peak Direction',
               'Wind Average (knots)','Wind Prevailing Direction',
               'Precipitation Melted (mm)','Precipitation Snow (cm)','Depth at Snowstake (cm)',
               'Sea Temp/Ice'];
head_201310 = ['Day','Temperature High (C)','Temperature Low (C)','Temperature Average (C)',
               'Pressure High (mbar)','Pressure Low (mbar)','Pressure Average (mbar)',
               'Wind 5-Sec Peak (knots)','Wind 2-Min Peak (knots)','Wind 2-Min Peak Direction',
               'Wind Average (knots)','Wind Prevailing Direction',
               'Precipitation Melted (mm)','Precipitation Snow (cm)','Depth at Snowstake (cm)',
               'Sea Surface Temperature (C)','Sea Ice (WMO Code)'];
head_201606 = ['Day','Temperature High (C)','Temperature Low (C)','Temperature Average (C)',
               'Pressure High (mbar)','Pressure Low (mbar)','Pressure Average (mbar)',
               'Wind 5-Sec Peak (knots)','Wind 5-Sec Peak Direction',
               'Wind Average (knots)','Wind Prevailing Direction',
               'Precipitation Melted (mm)','Precipitation Snow (cm)','Depth at Snowstake (cm)',
               'Sea Surface Temperature (C)','Sea Ice (WMO Code)']

# Force selected columns to be strings
dtypes = {
  'Precipitation Melted (mm)':str,
  'Precipitation Snow (cm)':str,
  'Depth at Snowstake (cm)':str,
  'Sea Ice (WMO Code)':str,
  'Sea Temp/Ice':str,
}

def convert_sst(x):
  s = str(x)
  if (s != 'nan') & (len(s)>5):
    t = s.zfill(10)[-10:-5]
    if t[-5:-3]=='00':
      s = float(t[-3:])/10
    elif t[-5:-3]=='01':
      s = float(t[-3:])/10 * -1
    else:
      s = '' # 'Parse Error' + s
  else:
    s = ''
  return s
  
def convert_ice(x):
  s = str(x)
  if(s != 'nan'):
    return str(x).zfill(10)[-5:]

# Function to trim only strings
# https://stackoverflow.com/questions/33788913/pythonic-efficient-way-to-strip-whitespace-from-every-pandas-data-frame-cell-tha
def remove_whitespace(x):
  if isinstance(x, str):
    return x.strip()
  else:
    return x

# Primary function
def main():
  
  # Step 1 - Load cleaned climatology files using Climatology File Index
  input_dir = 'climatology_cleaned'
  months = pd.read_csv(input_dir + '/climatology_files.csv')
  out = []
  for row in months.itertuples():
    year = '%d' % row.Year
    month = ('%d' % row.Month).zfill(2)
    ym = year + month
    filename = '%s/%s/WX%s.PRN' % (input_dir, year, ym)
    # print('Processing file %s' % filename)
    
    if (ym < '200310'):
      header = head_198904
    elif ((ym >= '200310') & (ym < '200405')):
      header = head_200310
    elif ((ym >= '200405') & (ym < '201310')):
      header = head_200405
    elif ((ym >= '201310') & (ym < '201606')):
      header = head_201310
    elif (ym >= '201606'):
      header = head_201606
    else:
      header = []
    
    df = [] #Clear dataframe
    if (row.StartLine):
      if ym in ['201610','201611','201612',
                '201701','201703','201707','201708','201709',
                '201808','201811','201812',
                '201904','201902','202109',
                '202110','202111']:
        df = pd.read_csv(filename, skiprows=row.StartLine, header=None, names=header, sep='\t', na_values=['M'], dtype=dtypes)
      else:
        df = pd.read_fwf(filename, skiprows=row.StartLine, header=None, names=header, na_values=['M'], dtype=dtypes)
      if (df.Day[0] == 1):
        df['Year'] = row.Year
        df['Month'] = row.Month
        out.append(df)
      else:
        print('INCORRCT START DATE with file %s' % filename)
        print(df.head())
        
      # Check for missing Sea Ice Values
      if (ym < '201310'):
        if (df['Sea Temp/Ice'].isnull().values.any()):
          print('Missing Sea Temp/Ice in %s, %s values' % (filename, df['Sea Temp/Ice'].isnull().sum()) )
      if (ym >= '201310'):
        if (df['Sea Ice (WMO Code)'].isnull().values.any()):
          print('Missing Sea Ice in %s, %s values' % (filename, df['Sea Ice (WMO Code)'].isnull().sum()))
          
      # Split combined SST/Ice values in older files
      if (ym < '201310'):
        df['Sea Ice (WMO Code)'] = df['Sea Temp/Ice'].apply(convert_ice)
        df['Sea Surface Temperature (C)'] = df['Sea Temp/Ice'].apply(convert_sst)
    else:
      print('UNDEFINED START LINE - Skipping file %s' % filename)
  
  # Step 2 - Load the more recent climatology files
  # Grab the list of files to process
  files = glob.glob('climatology/*/*.PRN')
  files = sorted(files)
  
  for filename in files:
    year = filename[-10:-6]
    month = filename[-6:-4]
    ym = year + month
    # print('Processing file %s' % filename)

    header = head_201606
    df = [] #Clear dataframe
    df = pd.read_csv(filename, skiprows=47, header=None, names=header, sep='\t', na_values=['M'], encoding='utf-16', dtype=dtypes)
    
    if (df.Day[0] == 1):
      df['Year'] = year
      df['Month'] = month
      out.append(df)
    else:
      print('INCORRCT START DATE with file %s' % filename)
      print(df.head())
        
    if (df['Sea Ice (WMO Code)'].isnull().values.any()):
      print('Missing Sea Ice in %s, %s values' % (filename, df['Sea Ice (WMO Code)'].isnull().sum()))
    
  
  # Step 3 - Merge the whole enchilada
  print('Finishing Up...')
  out2 = pd.concat(out, axis=0, ignore_index=True)
    
  # Add Date
  out2['Date'] = pd.to_datetime({'Year':out2.Year,'Month':out2.Month,'Day':out2.Day})
  out2.drop(columns={'Year','Month','Day'}, inplace=True)
  
  # Trim spaces on strings
  out2 = out2.map(lambda x: remove_whitespace(x) )
    
  # Expected Column Order
  cols = ['Date','Temperature High (C)','Temperature Low (C)','Temperature Average (C)',
          'Sea Surface Temperature (C)','Sea Ice (WMO Code)','Pressure High (mbar)','Pressure Low (mbar)',
          'Pressure Average (mbar)','Wind Peak (knots)','Wind 5-Sec Peak (knots)','Wind 2-Min Peak (knots)',
          'Wind Average (knots)','Wind Peak Direction',
          'Wind 5-Sec Peak Direction','Wind 2-Min Peak Direction','Wind Prevailing Direction',
          'Precipitation Melted (mm)','Precipitation Snow (cm)','Depth at Snowstake (cm)','Sky Coverage (tenths)']
    
  # Add Missing Columns
  missing = [c for c in cols if c not in out2.columns]
  print('Missing Columns: %s' % missing)
  for miss in missing:
    out2[miss] = ''
    
  # Identify Extra Columns
  extra = [c for c in out2.columns if c not in cols]
  print('Extra Fields: %s' % extra)
    
  # Reorder Columns (preserving extra columns at the end)
  out2 = out2[cols + [c for c in out2.columns if c not in cols]]
    
  # Drop Extra Columns
  out2.drop(columns=extra, inplace=True)
    
  # Export
  out2.to_csv(args.fname,index=False)
  print('Output file: %s' %args.fname)
  
  
# Main function for command line mode
if __name__ == '__main__':
  # Command Line Arguments
  parser = argparse.ArgumentParser(description='PAL Daily Climatology Compiler')
  parser.add_argument('-f','--fname', type=str,
    default='PalmerStation_Daily_Weather.csv',
    help='Output filename')
  args = parser.parse_args()
  main()
