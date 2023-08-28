# Script to copy Palmer Station Weather data from AMRC at UW-Madison
# Sage Lichtenwalner, Rutgers University
# Revised 6/30/2023
#
# For more information about the weather archive, see
#   AMRC Palmer Station Meteorology Information
#   https://amrc.ssec.wisc.edu/usap/palmer/
#
# This script is designed to be used on a Mac.
# First, create a mount point using "Connect to Server" in Finder
# Use the following server address, and connect as a "Guest"
#   ftp://amrc.ssec.wisc.edu/pub/palmer/
# Thanks to this trick, you can now use a rsync "locally" to grab all the files over FTP
#
# Note, AMRC is planning to deprecate FTP, so this will likely change in the near future.


# Full Directories
rsync -avz --delete /Volumes/palmer/climat ./weather_amrc
rsync -avz --delete /Volumes/palmer/climatology ./weather_amrc
rsync -avz --delete /Volumes/palmer/seasurfobs_snowacc ./weather_amrc
rsync -avz --delete /Volumes/palmer/waterwall ./weather_amrc

# Specific Years for large folders
rsync -avz --delete /Volumes/palmer/observations/2022 ./weather_amrc/observations/
rsync -avz --delete /Volumes/palmer/observations/2023 ./weather_amrc/observations/
rsync -avz --delete /Volumes/palmer/tidegauge/2022 ./weather_amrc/tidegauge/
rsync -avz --delete /Volumes/palmer/tidegauge/2023 ./weather_amrc/tidegauge/
