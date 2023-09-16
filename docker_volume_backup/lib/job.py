import datetime
import logging
from venv import create

from typing import List


from docker_volume_backup.lib.s3 import S3Client
from docker_volume_backup.lib.volume import Volume
from docker_volume_backup.lib.stfp import SFTP
from docker_volume_backup.lib.smb import SMBClient
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
        for volume in self.volumes:
            try:
                logging.info("Processing %s ", volume)
                volume = Volume(volume)
                volume.create_tarfile()
                volume.create_backup_record()
                for mode in self.modes:
                    if mode == 'S3':
                        s3_client = S3Client()
                    elif mode == 'SFTP':
                        sftp_client = SFTP()
                    elif mode == 'SMB':
                        smb_client = SMBClient()
                    if mode == 'S3':
                        s3_client.upload_object(path=volume.filename, key=volume.filename)
                        logging.info("Backup saved to S3")
                    elif mode == 'SFTP':
                        sftp_client.save_file_sftp(filepath=volume.filename, filename=volume.filename)
                        logging.info("Backup saved to SFTP")
                    elif mode == 'SMB':
                        smb_client.save_file(filepath=volume.filename, filename=volume.filename)
                        logging.info("Backup saved to SMB")
                backups_to_delete = volume.old_backups()
                for backup in backups_to_delete:
                    for mode in self.modes:
                        if mode == 'S3':
                            try:
                                s3_client.delete_object(str(backup[1]))
                            except:
                                logging.exception('Error deleting %s from S3', backup[1])
                        elif mode == 'SFTP':
                            try:
                                sftp_client.delete_file(str(backup[1]))
                            except:
                                logging.exception("Error deleting %s from SFTP", backup[1])
                        elif mode == "SMB":
                            try:
                                smb_client.delete_file(str(backup[1]))
                            except:
                                logging.exception("Error deleting %s from SMB", backup[1])
                    volume.delete_backup_record(backup_id=str(backup[0]))
                volume.delete_tarfile()
            except:
                logging.exception("Error processing volume")