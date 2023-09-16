import pysftp
import os
import logging

class SFTP:
    def __init__(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        self.sftp_connection = pysftp.Connection(host=os.environ["STORAGE-SERVER"], username=os.environ['USERNAME'], password=os.environ['PASSWORD'], port=int(os.environ['PORT']), cnopts=cnopts)


    def save_file_sftp(self, filepath: str, filename: str) -> None:
        with self.sftp_connection as sftp:
            dir_list= sftp.listdir()
            logging.error(dir_list)
            remoteFilePath = "/" + filename
            sftp.put(filepath, remoteFilePath)


    def delete_file(self, filename: str) -> None:
        with self.sftp_connection as sftp:
            remoteFilePath = "/" + filename
            sftp.remove(remoteFilePath)
