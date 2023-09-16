from freezegun import freeze_time

def test_job_import():
    from docker_volume_backup.lib.job import Job
    assert True


def test_job_creation():
    from docker_volume_backup.lib.job import Job
    test_modes = ["S3"] 
    test_volumes = ["test1, test2"]
    job = Job(test_modes, test_volumes)
    assert type(job) == Job
    assert job.modes == test_modes
    assert job.volumes == test_volumes
