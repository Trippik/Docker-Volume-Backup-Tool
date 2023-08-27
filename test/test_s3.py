from moto import mock_s3
import os

def test_s3_import():
    from docker_volume_backup.lib.s3 import S3Client
    assert True

@mock_s3
def test_client_creation():
    from docker_volume_backup.lib.s3 import S3Client
    os.environ["ACCESS-KEY-ID"] = "AKIAIOSFODNN7EXAMPLE"
    os.environ["SECRET-KEY"] = "bPxRfiCYEXAMPLEKEY"
    os.environ["BUCKET"] = 'test-bucket'
    s3_client = S3Client()
    assert s3_client.bucket == "test-bucket"
    assert str(type(s3_client.client)) == "<class 'botocore.client.S3'>"

@mock_s3
def test_upload_object():
    from docker_volume_backup.lib.s3 import S3Client
    os.environ["ACCESS-KEY-ID"] = "AKIAIOSFODNN7EXAMPLE"
    os.environ["SECRET-KEY"] = "bPxRfiCYEXAMPLEKEY"
    os.environ["BUCKET"] = 'test-bucket'
    s3_client = S3Client()
    s3_client.client.create_bucket(Bucket="test-bucket")

    f = open("demofile3.txt", "w")
    f.write("Woops! I have deleted the content!")
    f.close()

    s3_client.upload_object("demofile3.txt", "demofile3.txt")
    assert True

@mock_s3
def test_list_objects_in_bucket():
    from docker_volume_backup.lib.s3 import S3Client
    os.environ["ACCESS-KEY-ID"] = "AKIAIOSFODNN7EXAMPLE"
    os.environ["SECRET-KEY"] = "bPxRfiCYEXAMPLEKEY"
    os.environ["BUCKET"] = 'test-bucket'
    s3_client = S3Client()
    s3_client.client.create_bucket(Bucket="test-bucket")

    f = open("demofile3.txt", "w")
    f.write("Woops! I have deleted the content!")
    f.close()

    s3_client.upload_object("demofile3.txt", "demofile3.txt")
    objects_in_bucket = s3_client.list_objects_in_bucket()
    assert objects_in_bucket == ["demofile3.txt"]

@mock_s3
def test_delete_object_in_bucket():
    from docker_volume_backup.lib.s3 import S3Client
    os.environ["ACCESS-KEY-ID"] = "AKIAIOSFODNN7EXAMPLE"
    os.environ["SECRET-KEY"] = "bPxRfiCYEXAMPLEKEY"
    os.environ["BUCKET"] = 'test-bucket'
    s3_client = S3Client()
    s3_client.client.create_bucket(Bucket="test-bucket")

    f = open("demofile3.txt", "w")
    f.write("Woops! I have deleted the content!")
    f.close()

    s3_client.upload_object("demofile3.txt", "demofile3.txt")
    s3_client.delete_object("demofile3.txt")
    objects_in_bucket = s3_client.list_objects_in_bucket()
    assert len(objects_in_bucket) == 0