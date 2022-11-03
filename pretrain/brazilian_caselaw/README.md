# How-to

The python script ```run_scrapers_in_parallel.py``` will start the downloading. It will generate R-scripts for different years, currently 2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022 and download from the beginning of January to the end of December. The R-scripts are generated from the template ```script_template.R```. If you want to include more years (currently, this does not make sense), you can add them in the script ```run_scrapers_in_parallel.py```. 

When starting the script, you can provide the argument ```-dnb```, i.e. ```--download_boolean```. It takes either 'TRUE' or 'FALSE'. The default value is 'TRUE'. When set to 'TRUE', the scripts will download and conver the HTML files to json. If set to 'FALSE', only the conversion to json happens. 