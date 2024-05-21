PALMER STATION, ANTARCTICA

PAWS AUTOMATED WEATHER DATA SYSTEM
PALMER STATION, ANTARCTICA

A Description of the Archived Data

Updated September 2022 by B. Rosen-Filardo (Palmer RA)
----------------------------------------------------------------------

Data files and station locations:

	ARYYMMDD.100 - The weather station on Gamage Point (dismantled 2017)

	ARYYMMDD_BASE.txt - The new weather station in the "backyard" of Palmer Station

	ARYYMMDD_AWS1.txt - The weather station on Wauwermans Islands (8 miles from Palmer Station, Lat -64.918 Long -64.049) - Installed Oct 31 2015

	ARYYMMDD_AWS2.txt - The weather station in the Joubins Island group, on Howard Island (Lat -64.786987 Long -64.360658)

	ARYYMMDD_AWS3.txt - The weather station in the Gosslers Island group (Lat -64.712916 Long -64.348396)

------------------------------------------------------------------------

File name: ARyymmdd.xxx, where AR stands for Archive, and xxx is the
station number.

1st row: Column Headings.  The units for each heading are listed below,
followed by a general description of the data, if any.


A description of the archived data files. This is for the automated station that went on line in September 2015.

Filename: ARYYMMDD_UnitID.txt
	where	AR = Archive
		YY = Year
		MM = Month
		DD = Day
		UnitID = Station identification. Can be AWS1, AWS2, AWS3, or BASE.


Column	Label			Description
------	-----			-----------
  1	SampleDateTime		Date and time (UTC)

  2	Unit ID			The location of the weather station.

  3	WS Avg 2min		Wind speed, 1 min average, m/sec
				RM Young, Model 05108-45

  4	WD Avg 2min		Wind direction for 1 min average

  5	WGS 10min		Wind gust speed, 10 min, m/sec

  6	WGD 10min		Wind gust direction

  7	Air Temp		Air temperature, degrees C
				Rotronic, HC2S3, Hygroclip 2, Temp/RH

  8	Rel Humidty		Relative humidity, %
				Rotronic, HC2S3, Hygroclip 2, Temp/RH

  9	Dew Point		Dew point, calculated from temp and RH, degrees C

  10	Pyranometer		Solar irradiance, W/m^2
				Licor, LI-200R

  11	Quantum			Photosynthetically active radiation, uMol/sec/m^2
				Licor, LI-190
  
  12	Air Pressure		Atmospheric pressure, mbar
				Honeywell, HPA200

  13	Snow Level		No sensor installed

  14	Rainfall		Melted precipitation, mm
				Mesotech, MT-PA01D 8" heated, tipping rain bucket. Measures rainfall and melted snow/sleet. 
				Each tip of the bucket corresponds to 0.254mm of precipitation.

  15	PW Current		Present weather
				Optical Scientific, Inc. OWI-430 WIVIS
				The code is from Table 12-2 of Federal Meteorological Handbook No. 1. This sensor
				cannot detect hail. 

  16	Visibility		Visibility, m
				Optical Scientific, Inc. OWI-430 WIVIS
				Maximum range is 10 km.

  17	CBase1			Cloudbase, lower level, feet
				Mesotech ceilometer, CBME80. This device measures cloud height using LIDAR. A pulsed
				light beam is directed vertically and the return signal is detected. Depending on the 
				nature of that return, distinct cloud layers may be detected: lower, middle and upper.
				If there is no distinct return (due to fog, for instance), vertical visibility is
				reported.

  18	CBase2			Cloudbase, middle level, feet

  19	CBase3			Cloudbase, upper level, feet

  20	Vert Vis		Vertical visibility, feet


The *.100 files are no longer available starting October 2017. There are
4 new files that have been transmitted that provide the daily Palmer
observations: AWS1, AWS2, AWS3 and BASE files.

AWS1 and the BASE files are available starting November 2015.
AWS2 files are available starting March 2016 and AWS3 files are available
starting August 2016.

----------------------------------------------------------------------
