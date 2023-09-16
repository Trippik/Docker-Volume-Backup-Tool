import os
os.environ["DB-FILEPATH"] = 'test.db'

def test_db_import():
    from docker_volume_backup.lib.db import Database
    assert True

def test_create_db_object():
    from docker_volume_backup.lib.db import Database
    db = Database()
    assert True

def test_run_command():
    from docker_volume_backup.lib.db import Database
    db = Database()
    command = "INSERT INTO volumes (volume_name) VALUES ('test-volume');"
    db.run_command(command=command)
    assert True

def test_run_query():
    from docker_volume_backup.lib.db import Database
    db = Database()
    query = "SELECT * FROM volumes"
    results = db.run_query(query=query)
    assert 'test-volume' in str(results)
