import os
os.environ["DB-FILEPATH"] = 'test.db'
os.environ["DB-TYPE"] = 'SQLite'

def test_db_import():
    from docker_volume_backup.lib.db import SQLiteDatabase
    assert True

def test_create_db_object():
    from docker_volume_backup.lib.db import SQLiteDatabase
    db = SQLiteDatabase()
    assert True

def test_run_command():
    from docker_volume_backup.lib.db import SQLiteDatabase
    db = SQLiteDatabase()
    command = "INSERT INTO volumes (volume_name) VALUES ('test-volume');"
    db.run_command(command=command)
    assert True

def test_run_query():
    from docker_volume_backup.lib.db import SQLiteDatabase
    db = SQLiteDatabase()
    query = "SELECT * FROM volumes"
    results = db.run_query(query=query)
    assert 'test-volume' in str(results)
