import datetime
from freezegun import freeze_time
import os
import os
os.environ["DB-FILEPATH"] = 'test-vol.db'
if os.path.isfile(os.environ["DB-FILEPATH"]):
    os.remove(os.environ["DB-FILEPATH"])

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
