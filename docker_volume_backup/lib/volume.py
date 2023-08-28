import os
import datetime
import logging
import tarfile

class Volume:
    def __init__(self, volume_path):
        self.volume_path = volume_path
        self.filepath = self.generate_file_path()
        self.filename_without_date = self.sanitize_file_path()
        self.filename = self.generate_file_name()

    def generate_file_path(self) -> str:
        filename = self.volume_path + '_' + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = filename + ".tar.gz"
        return(filename)

    def sanitize_file_path(self) -> str:
        return(self.volume_path.replace('/', '-'))

    def generate_file_name(self) -> str:
        filename = self.volume_path + '_' + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = filename + ".tar.gz"
        return(filename.replace('/', '-'))
    
    def create_tarfile(self) -> None:
        with tarfile.open(self.filename, "w:gz") as tar:
            tar.add(self.volume_path, arcname="")

    def delete_tarfile(self) -> None:
        os.remove(self.filename)