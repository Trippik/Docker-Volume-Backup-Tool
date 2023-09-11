import datetime
import logging
from venv import create

from typing import List


from docker_volume_backup.lib.s3 import S3Client
from docker_volume_backup.lib.volume import Volume
from docker_volume_backup.lib.ftp import FTP
from docker_volume_backup.lib.stfp import SFTP
class Job:
    def __init__(self, modes: List[str], volumes: list) -> None:
        self.foldername = self.generate_folder_name()
        self.modes = modes
        self.volumes = volumes

    def generate_folder_name(self) -> str:
        foldername = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        return(foldername)

    def run(self) -> None:
        logging.info("Starting job")
        for mode in self.modes:
            if mode == 'S3':
                s3_client = S3Client()
            elif mode == 'FTP':
                ftp_client = FTP()
            elif mode == 'SFTP':
                sftp_client = SFTP()
            for volume in self.volumes:
                logging.info("Processing %s ", volume)
                volume = Volume(volume)
                volume.create_tarfile()
                volume.create_backup_record()
                if mode == 'S3':
                    s3_client.upload_object(path=volume.filename, key=volume.filename)
                    logging.info("Backup saved to S3")
                elif mode == 'SFTP':
                    sftp_client.save_file_sftp(filepath=volume.filename, filename=volume.filename)
                    logging.info("Backup saved to SFTP")
                elif mode == 'FTP':
                    ftp_client.save_file_ftp(filepath=volume.filename, filename=volume.filename)
                    logging.info('Backup saved to FTP')
                backups_to_delete = volume.old_backups()
                if mode == 'S3':
                    for backup in backups_to_delete:
                        s3_client.delete_object(str(backup[1]))
                        volume.delete_backup_record(backup_id=str(backup[0]))
                if mode == 'SFTP':
                    for backup in backups_to_delete:
                        sftp_client.delete_file(str(backup[1]))
                        volume.delete_backup_record(backup_id=str(backup[0]))
                volume.delete_tarfile()