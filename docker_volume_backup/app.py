#------------------------------------
#LIBRARIES AND SETUP
#------------------------------------
#Import necessary libraries
import datetime
import os
import logging
from venv import create
import ast

from docker_volume_backup.lib.job import Job

#Basic setup
vol_directory = "/vols_path/"
modes = os.environ["TARGET-MODES"]
modes = ast.literal_eval(modes)
logging.basicConfig(level=logging.INFO)

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
                if "FTP" and "SFTP" in modes:
                    logging.error('Only FTP or SFTP permitted when running multiple jobs, not running the FTP job')
                    running_modes = modes
                    running_modes.remove('FTP')
                else:
                    running_modes = modes
                for mode in running_modes:
                    try:
                        logging.info("Saving backups to %s", mode)
                        job = Job(mode, vol_directory)
                        job.run()
                    except Exception:
                        logging.exception("Error when completing backup to %s", mode)
                run_state = 1
                logging.warning("---------------------")
        elif(int(datetime.datetime.now().strftime("%H")) != int(os.environ["REPORTING_HOUR"]) and run_state == 1):
            run_state = 0

if __name__ == '__main__':
    main()
