import sqlite3
from sqlite3 import OperationalError
import os
import logging
import psycopg2

class PostgreSQLDatabase:
    def __init__(self) -> None:
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()
        self.build_db()
    
    def create_connection(self):
        conn = psycopg2.connect(
            host=os.environ["DB-HOST"],
            database=os.environ["DB-SCHEMA"],
            user=os.environ["DB-USER"],
            password=os.environ["DB-PASSWORD"],
            port=os.environ["DB-PORT"])
        return conn
    

    def build_db(self) -> None:
        schema_filepath = "postgres-schema.sql"
        self.run_commands_from_file(schema_filepath)

    def run_command(self, command: str) -> None:
        logging.info(f"Running command: {command}")
        try:
            self.cursor.execute(command)
            self.conn.commit()
        except Exception as msg:
            logging.exception(f"Command skipped: {msg}")

    def run_query(self, query: str) -> tuple:
        logging.info(f"Running query {query}")
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except Exception as msg:
            logging.exception(f"Command skipped: {msg}")
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

class SQLiteDatabase:
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
        schema_filepath = "sqlite-schema.sql"
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

if os.environ["DB-TYPE"] == "SQLite":
    db = SQLiteDatabase()
elif os.environ["DB-TYPE"] == "PostgreSQL":
    # If set to PostgreSQL and an SQLite DB file is present migrate data
    if os.path.isfile(os.environ['DB-FILEPATH']):
        old_db = SQLiteDatabase()
        new_db = PostgreSQLDatabase()
        
        volume_records = old_db.run_query("SELECT * FROM volumes")
        for record in volume_records:
            new_db.run_command(str(f"INSERT INTO volumes (id, volume_name) VALUES ({record[0]}, '{record[1]}')"))
        
        backup_records = old_db.run_query("SELECT * FROM backups")
        for record in backup_records:
            new_db.run_command(str(f"INSERT INTO backups (id, backup_name, volume, backup_date) VALUES ({record[0]}, '{record[1]}', {record[2]}, '{record[3]}')"))
        
        os.remove(os.environ['DB-FILEPATH'])
        db = new_db
    else:
        db = PostgreSQLDatabase()