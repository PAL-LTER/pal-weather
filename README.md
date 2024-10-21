# Palmer LTER Weather Archive

This repository includes the processed datafiles and code needed to aggregate the long-term weather timeseries datasets for the [Palmer LTER](http://pallter.marine.rutgers.edu) project.  The raw data from the Palmer Station Antarctica weather tower is collected by NSF-contractors (Palmer Station research associates), and archived in the [AMRDC Data Repository](https://amrdcdata.ssec.wisc.edu/group/palmer-station).  This repo includes an edited copy of that archive, along with scripts to merge and average the full dataset for research use.  The processed [daily](https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-pal.28.10) and [monthly](https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-pal.189.10) datasets are archived on the Environmental Data Initiative’s data repository.

Note, there have been a series of weather towers and instruments deployed at the station (see the docs directory).  Care must be used when interpreting long-term trends, as these instrument changes may impact data comparability.

This repo is currently managed by Sage Lichtenwalner, PAL Information Manager, Rutgers University

## Repository Contents
Here are the key directories and files in this repo:
* [climatology](climatology) - Newer daily climatology files from Palmer/AMRDC (as of Jan 2017) have been reproduced in a consistent format, and therefore do not need any editing.  They can be simply copied into this directory for processing.
* [climatology_cleaned](climatology_cleaned) - Older climatology files changed format often.  This directory includes manually edited files to streamline the format to facilitate loading via the process script.
* [climatology/climatology_files.csv](climatology/climatology_files.csv) - This index file is used to specify which older cleaned files should be included.
* [docs](docs) - Reference information on the Palmer Station weather dataset.
* compare_* - Rough scripts to compare a new CSV dataset to a prior version on EDI.
* process_* - Scripts used to create new merged CSVs for archving.

## Processing Steps
This dataset is typically updated every year, after the austral summer field season.  Use these steps to update the datasets.

1. Download the latest [Palmer Station climatology summary data](https://amrdcdata.ssec.wisc.edu/dataset/palmer-station-climatology-summary-data) from AMRDC.  Place the newer files into the `climatology` directory. 
2. Run the `process_climatology.py` script.  (No changes should be necessary, unless the datafile format has changed or a different aggregation approach is required.)
3. Optional: Update the `compare_daily.py` script to point to the latest archived dataset on EDI.  (Make sure the input and output filenames are correct.)  Review the output to make sure the updates are correct.
4. Run the `process_monthly.py` script/
5. Optional: Update the `compare_monthly.py` script to point to the latest archived dataset on EDI.  (Make sure the input and output filenames are correct.)  Review the output to make sure the updates are correct.
6. If desired, move the new archive files into a data_# directory.
7. Use ezEML to update the metadata for the new datasets for archiving.
