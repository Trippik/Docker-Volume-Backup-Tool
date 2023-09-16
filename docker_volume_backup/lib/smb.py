import os
from smb.SMBConnection import SMBConnection
import logging

class SMBClient:
    def __init__(self) -> None:
        self.share_name = os.environ["SMB-SHARE"]
        self.client = SMBConnection(username=os.environ['USERNAME'], password=os.environ['PASSWORD'], remote_name=self.share_name,my_name="")
        if self.client.connect(ip=os.environ["STORAGE-SERVER"]):
            logging.info("SMB Connection successful")
        else:
            logging.error("SMB Connection error")


    def save_file(self, filepath: str, filename:str) -> None:
        file = open(filepath, 'rb')
        with file:
            self.client.storeFile(service_name=self.share_name, path=filename, file_obj=file)
    
    def delete_file(self, filename:str) -> None:
        self.client.deleteFiles(self.share_name, filename)