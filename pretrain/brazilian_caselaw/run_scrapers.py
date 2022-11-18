from multiprocessing import Pool
import os
import re
import argparse

base_name = "scraper_for_brazilian_court_decisions_for_year_"


def delete_existing_scripts():
    
    files = os.listdir('.')
    generated_R_scripts_previously = [x for x in files if x.startswith(base_name)]
    for script in generated_R_scripts_previously:
        os.remove(script)



def generate_scripts(list_of_years, download_boolean):

    delete_existing_scripts()
    
    for year in list_of_years:
        year = str(year)
        r_script_template = open("script_template.R", "r").read()
        r_script_template_with_year = re.sub(r'{YEAR}', year, r_script_template)
        r_script_template_with_year = re.sub(r'{DOWNLOAD_BOOLEAN}', download_boolean, r_script_template_with_year)

        with open(base_name + str(year) + ".R", "w") as f:
            print(r_script_template_with_year, file=f)


def run_script(r_script):
    command = 'Rscript ' + r_script
    print(command)
    os.system(command)


def run_in_parallel(commands_to_run):
    if len(commands_to_run) > 0:
        pool = Pool(processes=len(commands_to_run))
        pool.map(run_script, commands_to_run)


def run_sequentially(commands_to_run):
    for command in commands_to_run:
        run_script(command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-dnb', '--download_boolean',
                        help='Define whether you want to download or only to convert to json.', default="TRUE")
    parser.add_argument('-rp', '--run_in_parallel', type=lambda x: (str(x).lower() == 'true'),
                        help='Define whether you want to run the years in parallel', default=True)

    args = parser.parse_args()

    years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    generate_scripts(years, args.download_boolean)
    all_files = os.listdir('./')
    all_r_scripts = [x for x in all_files if x.endswith('.R') and base_name in x and bool(re.search(r'\d', x))]
    if args.run_in_parallel:
        run_in_parallel(all_r_scripts)
    else:
        run_sequentially(all_r_scripts)  # do this if you don't have enough RAM
