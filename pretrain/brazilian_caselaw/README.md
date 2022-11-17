# How-to

The python script ```run_scrapers_in_parallel.py``` will start the downloading. It will generate R-scripts for different years, currently 2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022 and download from the beginning of January to the end of December. The R-scripts are generated from the template ```script_template.R```. If you want to include more years (currently, this does not make sense), you can add them in the script ```run_scrapers_in_parallel.py```. 

When starting the script, you can provide the argument ```-dnb```, i.e. ```--download_boolean```. It takes either 'TRUE' or 'FALSE'. The default value is 'TRUE'. When set to 'TRUE', the scripts will download and conver the HTML files to json. If set to 'FALSE', only the conversion to json happens. 

## Caution!
```script_template.R``` uses the method tjsp_baixar_cjsg which download only the syllabus, but not the entire opinion. The opinions are published as PDFs. In oder to download the opintions, you need to apply ```download_entire_opinion.R```. Unfortunately,  [https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do?f=1]( https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do?f=1) will pop up captchas when clicking on the PDFs. To be able to bypass these captchas and, consequently, download the PDFs, you need to have an account, i.e. a username and a password

You need to provide the following commandline arguments to run the script:
 - username: username to log in to [https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do?f=1]( https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do?f=1)
 - password: password to log in to [https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do?f=1]( https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do?f=1)
 - input_path : the path where all donwloaded HTML files are saved
 - output_path: the path where you want to save the downloaded PDFs. This directory will be created automatically if it does not already exist.

So, to run the script, you can type this:

```
Rscript download_entire_opinion.R {USERNAME} {PASSWORD} {INPUT_PATH} {OUTPUT_PATH} 
```

One a concrete, fake example:

```
Rscript download_entire_opinion.R user_xy password123 cjsg__01-01-2022__03-01-2022 cjsg__01-01-2022__03-01-2022_pdfs 
```
