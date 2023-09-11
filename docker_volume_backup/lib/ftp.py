import ftplib
import os

class FTP:
    def __init__(self):
      self.session = ftplib.FTP(os.environ["STORAGE-SERVER"],os.environ['USERNAME'],os.environ['PASSWORD'])

    def save_file_ftp(self, filepath: str, filename: str) -> None:
        file = open(filepath,'rb')
        self.session.storbinary('STOR ' + filename, file)
        file.close()
        self.session.quit()
    
