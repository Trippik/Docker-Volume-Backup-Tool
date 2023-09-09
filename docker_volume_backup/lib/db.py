import sqlite3
from sqlite3 import OperationalError
import os
import logging

class Database:
    def __init__(self) -> None:
        self.filepath = os.environ['DB-FILEPATH']
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()
        self.build_db()
        

    def db_exists(self) -> None:
        return os.path.isfile(self.filepath)
    
    
    def create_connection(self):
        conn = sqlite3.connect(self.filepath)
        return conn
    

    def build_db(self) -> None:
        schema_filepath = "schema.sql"
        self.run_commands_from_file(schema_filepath)

    def run_command(self, command: str) -> None:
        try:
            self.cursor.execute(command)
            self.conn.commit()
        except OperationalError as msg:
            logging.error(f"Command skipped: {msg}")

    def run_query(self, query: str) -> tuple:
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except OperationalError as msg:
            logging.error(f"Command skipped: {msg}")
        return(rows)

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
                self.run_command(command)
            except OperationalError as msg:
                logging.error("Command skipped: ", msg)

db = Database()