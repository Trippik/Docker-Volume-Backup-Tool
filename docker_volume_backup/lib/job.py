import os
import datetime
import logging
import tarfile
from venv import create
import ftplib
import pysftp

from typing import List


from docker_volume_backup.lib.s3 import S3Client
from docker_volume_backup.lib.volume import Volume
class Job:
    def __init__(self, modes: List[str], volumes: list) -> None:
        self.foldername = self.generate_folder_name()
        self.modes = modes
        self.volumes = volumes

    def generate_folder_name(self) -> str:
        foldername = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        return(foldername)

    def save_file_ftp(self, filename: str) -> None:
        session = ftplib.FTP(os.environ["STORAGE-SERVER"],os.environ['USERNAME'],os.environ['PASSWORD'])
        file = open(filename,'rb')
        session.storbinary('STOR ' + filename, file)
        file.close()
        session.quit()

    def save_file_sftp(self, filename: str) -> None:
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        with pysftp.Connection(host=os.environ["STORAGE-SERVER"], username=os.environ['USERNAME'], password=os.environ['PASSWORD'], port=int(os.environ['PORT']), cnopts=cnopts) as sftp:
            dir_list= sftp.listdir()
            logging.error(dir_list)
            remoteFilePath = "/" + filename
            sftp.put(filename, remoteFilePath)
        
    def save_file_s3(self, s3_client: S3Client, filepath: str, filename: str) -> None:
        logging.info("Starting upload of %s", filename)
        s3_client.upload_object(path=filepath, key=filename)


    def remove_old_files_ftp(self) -> None:
        logging.error("Automated deletion of backups is not yet supported using FTP")

    def remove_old_files_sftp(self) -> None:
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

    def run(self) -> None:
        logging.info("Starting job")
        for mode in self.modes:
            if mode == 'S3':
                s3_client = S3Client()
            for volume in self.volumes:
                logging.info("Processing %s ", volume)
                volume = Volume(volume)
                volume.create_tarfile()
                volume.create_backup_record
                if mode == 'S3':
                    self.save_file_s3(s3_client=s3_client, filepath=volume.filename, filename=str(volume.id))
                    logging.info("Backup saved to S3")
                elif mode == 'SFTP':
                    self.save_file_sftp(filename=volume.filename)
                    logging.info("Backup saved to SFTP")
                elif mode == 'FTP':
                    self.save_file_ftp(filename=volume.filename)
                    logging.info('Backup saved to FTP')
                backups_to_delete = volume.old_backups()
                if mode == 'S3':
                    for backup in backups_to_delete:
                        s3_client.delete_object(backup[0])
                        volume.delete_backup_record(backup_id=backup[0])
                volume.delete_tarfile()