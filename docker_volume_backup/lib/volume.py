import os
import datetime
import logging
import tarfile

from docker_volume_backup.lib.db import Database

db = Database()

class Volume:
    def __init__(self, volume_path):
        self.volume_path = volume_path
        self.datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        self.filepath = self._generate_file_path()
        self.filename_without_date = self._sanitize_file_path()
        self.filename = self._generate_file_name()
        self.id, _ = self._volume_record()

    def _generate_file_path(self) -> str:
        filename = self.volume_path + '_' + self.datetime
        filename = filename + ".tar.gz"
        return(filename)

    def _sanitize_file_path(self) -> str:
        return(self.volume_path.replace('/', '-'))
    
    def _generate_file_name(self) -> str:
        filename = self.volume_path + '_' + self.datetime
        filename = filename + ".tar.gz"
        return(filename.replace('/', '-'))
    
    def _db_record(self) -> tuple:
        query = f"SELECT * FROM volumes WHERE volume_name = '{self.filename_without_date}'"
        return db.run_query(query)
    
    def _db_record_exists(self) -> bool:
        exists = False
        if len(self._db_record()) > 0:
            exists = True
        return exists
    
    def _create_db_record(self) -> None:
        query = f"INSERT INTO volumes (volume_name) VALUES ('{self.filename_without_date}')"
        db.run_command(query)

    def _volume_record(self) -> tuple:
        if not self._db_record_exists():
            self._create_db_record()
        return self._db_record()[0]
        
    
    def create_tarfile(self) -> None:
        with tarfile.open(self.filename, "w:gz") as tar:
            tar.add(self.volume_path, arcname="")

    def write_backup_record(self) -> None:
        query = f"INSERT INTO backups (volume, backup_date) VALUES ({str(self.id)}, '{self.datetime}')"
        db.run_command(query)

    def delete_tarfile(self) -> None:
        os.remove(self.filename)