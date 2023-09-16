import datetime
from freezegun import freeze_time
import os
import os
os.environ["DB-FILEPATH"] = 'test-vol.db'
if os.path.isfile(os.environ["DB-FILEPATH"]):
    os.remove(os.environ["DB-FILEPATH"])
os.environ["NUMBER-OF-BACKUPS"] = "1"

def test_volume_import():
    from docker_volume_backup.lib.volume import Volume
    assert True

@freeze_time
def test_filepath_generation():
    from docker_volume_backup.lib.volume import Volume
    volume = Volume(volume_path='/test')
    assert volume.filepath == '/test_' + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + '.tar.gz'
    assert type(volume.filepath) is str

def test_filename_generation():
    from docker_volume_backup.lib.volume import Volume
    volume = Volume(volume_path='/test')
    assert volume.filename == '-test_' + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + '.tar.gz'
    assert type(volume.filename) is str

def test_backup_record():
    from docker_volume_backup.lib.volume import Volume
    from docker_volume_backup.lib.db import Database
    db = Database()
    volume = Volume(volume_path='/test')
    current_backups = int(db.run_query('SELECT COUNT(*) FROM backups')[0][0])
    volume.create_backup_record()
    assert int(db.run_query('SELECT COUNT(*) FROM backups')[0][0]) == current_backups + 1
    backup_db_entry = db.run_query('SELECT * FROM backups LIMIT 1')[0]
    assert len(backup_db_entry) == 4

def test_return_old_backup_records():
    from docker_volume_backup.lib.volume import Volume
    from docker_volume_backup.lib.db import Database
    db = Database()
    db.run_command("DELETE FROM backups") 
    volume = Volume(volume_path='/test')
    volume.create_backup_record()
    volume.create_backup_record()
    old_backups = volume.old_backups()
    assert len(old_backups) == 1
