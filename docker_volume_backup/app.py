#------------------------------------
#LIBRARIES AND SETUP
#------------------------------------
#Import necessary libraries
import datetime
import os
import logging
import tarfile
from venv import create
import ftplib
import pysftp

from docker_volume_backup.lib.job import Job

#Basic setup
vol_directory = "/vols_path/"
mode = os.environ["TARGET-MODE"]


#------------------------------------
#MAIN LOOP
#------------------------------------
def main():
    loop = True
    run_state = 0
    while(loop == True):
        if(int(datetime.datetime.now().strftime("%H")) == int(os.environ["REPORTING_HOUR"])):
            if(run_state == 0):
                logging.warning("Backup Starting")
                job = Job(mode, vol_directory)
                job.run()
                run_state = 1
                logging.warning("---------------------")
        elif(int(datetime.datetime.now().strftime("%H")) != int(os.environ["REPORTING_HOUR"]) and run_state == 1):
            run_state = 0

if __name__ == '__main__':
    main()
