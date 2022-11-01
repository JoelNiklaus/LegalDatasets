from multiprocessing import Pool
import os
import re


def run_script(r_script):
    command = 'Rscript '+r_script
    print(command)
    os.system(command)


def run_in_parallel(commands_to_run):
    if len(commands_to_run)>0:
        pool = Pool(processes=len(commands_to_run))
        pool.map(run_script, commands_to_run)



all_files = os.listdir('./')
all_r_scripts = [x for x in all_files if x.endswith('.R') and bool(re.search(r'\d',x))]


if __name__ =="__main__":
    run_in_parallel(all_r_scripts)