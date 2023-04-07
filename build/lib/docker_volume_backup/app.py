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


#Basic setup
vol_directory = "/vols_path/"
mode = os.environ["TARGET-MODE"]


#------------------------------------
#UNDERLYING FUNCTIONS
#------------------------------------
def generate_file_name():
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = filename + ".tar.gz"
    return(filename)

def create_backup_tar(filename):
    with tarfile.open(filename, "w:gz") as tar:
        tar.add(vol_directory, arcname=os.path.basename(vol_directory))

def save_file(filename):
    if(mode == "FTP"):
        session = ftplib.FTP(os.environ["STORAGE-SERVER"],os.environ['USERNAME'],os.environ['PASSWORD'])
        file = open(filename,'rb')
        session.storbinary('STOR ' + filename, file)
        file.close()
        session.quit()
    elif(mode == "SFTP"):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        with pysftp.Connection(host=os.environ["STORAGE-SERVER"], username=os.environ['USERNAME'], password=os.environ['PASSWORD'], port=int(os.environ['PORT']), cnopts=cnopts) as sftp:
            dir_list= sftp.listdir()
            logging.error(dir_list)
            remoteFilePath = "/" + filename
            sftp.put(filename, remoteFilePath)

def remove_old_files():
    if(mode == "FTP"):
        logging.error("Automated deletion of backups is not yet supported using FTP")
    elif(mode == "SFTP"):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        with pysftp.Connection(host=os.environ["STORAGE-SERVER"], username=os.environ['USERNAME'], password=os.environ['PASSWORD'], port=int(os.environ['PORT']), cnopts=cnopts) as sftp:
            max_no = int(os.environ["NUMBER-OF-BACKUPS"])
            dir_list= sftp.listdir()
            number_of_backups = len(dir_list)
            no_to_delete = number_of_backups - max_no
            count = 0 
            for file in dir_list:
                if(count < no_to_delete):
                    remoteFilePath = "/" + file
                    sftp.remove(remoteFilePath)
                count = count + 1



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
                filename = generate_file_name()
                create_backup_tar(filename)
                logging.warning("Backup Tar Created")
                save_file(filename)
                logging.warning("Backup Tar Sent to Server")
                os.remove(filename)
                remove_old_files()
                logging.warning("Old Backup Files Deleted")
                run_state = 1
                logging.warning("---------------------")
        elif(int(datetime.datetime.now().strftime("%H")) != int(os.environ["REPORTING_HOUR"]) and run_state == 1):
            run_state = 0

if __name__ == '__main__':
    main()
