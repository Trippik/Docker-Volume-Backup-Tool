import os
import datetime
import logging
import tarfile
from venv import create
import ftplib
import pysftp


from docker_volume_backup.lib.s3 import S3Client
class Job:
    def __init__(self, mode: str, vol_directory: str):
        self.filename = self.generate_file_name()
        self.mode = mode
        self.vol_directory = vol_directory



    def generate_file_name(self):
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = filename + ".tar.gz"
        return(filename)

    def create_backup_tar(self):
        with tarfile.open(self.filename, "w:gz") as tar:
            tar.add(self.vol_directory, arcname=os.path.basename(self.vol_directory))

    def save_file_ftp(self):
        session = ftplib.FTP(os.environ["STORAGE-SERVER"],os.environ['USERNAME'],os.environ['PASSWORD'])
        file = open(self.filename,'rb')
        session.storbinary('STOR ' + self.filename, file)
        file.close()
        session.quit()

    def save_file_sftp(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        with pysftp.Connection(host=os.environ["STORAGE-SERVER"], username=os.environ['USERNAME'], password=os.environ['PASSWORD'], port=int(os.environ['PORT']), cnopts=cnopts) as sftp:
            dir_list= sftp.listdir()
            logging.error(dir_list)
            remoteFilePath = "/" + self.filename
            sftp.put(self.filename, remoteFilePath)
        
    def save_file_s3(self, s3_client):
        s3_client.upload_object(self.filename, self.filename)


    def remove_old_files_ftp(self):
        logging.error("Automated deletion of backups is not yet supported using FTP")

    def remove_old_files_sftp(self):
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
    
    def remove_old_files_s3(self, s3_client):
        max_no = int(os.environ["NUMBER-OF-BACKUPS"])
        dir_list = s3_client.list_objects_in_bucket()
        number_of_backups = len(dir_list)
        no_to_delete = number_of_backups - max_no
        count = 0
        for file in dir_list:
            if(count < no_to_delete):
                s3_client.delete_object(file)
            count = count + 1

    def run(self):
        self.create_backup_tar()
        if self.mode == 'FTP':
            self.save_file_ftp()
            self.remove_old_files_ftp()
        elif self.mode == 'SFTP':
            self.save_file_sftp()
            self.remove_old_files_sftp()
        elif self.mode == 'S3':
            s3_client = S3Client()
            self.save_file_s3(s3_client)
            self.remove_old_files_s3(s3_client)
        os.remove(self.filename)