import os
import datetime
import logging
import tarfile

class Volume:
    def __init__(self, volume_path):
        self.volume_path = volume_path
        self.filename = self.generate_file_name()

    def generate_file_name(self) -> str:
        filename = self.volume_path + '_' + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = filename + ".tar.gz"
        return(filename)
    
    def create_tarfile(self) -> None:
        with tarfile.open(self.filename, "w:gz") as tar:
            tar.add(self.volume_path, arcname=os.path.basename(self.volume_path))

    def delete_tarfile(self) -> None:
        os.remove(self.filename)