import sqlite3
from sqlite3 import OperationalError
import os
import logging

class Database:
    def __init__(self) -> None:
        self.filepath = "/databases/volume_backup_tool.db"
        self.cursor = self.create_cursor()
        self.build_db()
        

    def db_exists(self) -> None:
        return os.path.isfile(self.filepath)
    

    def create_cursor(self) -> sqlite3.Cursor:
        conn = sqlite3.connect(self.filepath)
        return conn.cursor()
    

    def build_db(self) -> None:
        schema_filepath = "schema.sql"
        self.run_commands_from_file(schema_filepath)


    def run_commands_from_file(self, filepath: str) -> None:
        # Open and read the file as a single buffer
        fd = open(filepath, 'r')
        sqlFile = fd.read()
        fd.close()

        # all SQL commands (split on ';')
        sqlCommands = sqlFile.split(';')

        # Execute every command from the input file
        for command in sqlCommands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            try:
                self.cursor.execute(command)
            except OperationalError as msg:
                logging.error("Command skipped: ", msg)