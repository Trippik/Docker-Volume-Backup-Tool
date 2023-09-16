import boto3
import os

class S3Client:
    def __init__(self) -> None:
        access_key = os.environ["ACCESS-KEY-ID"]
        secret_key = os.environ["SECRET-KEY"]
        self.session = boto3.session.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.client = self.session.client('s3')
        self.bucket = os.environ["BUCKET"]

    def list_objects_in_bucket(self) -> list:
        response = self.client.list_objects_v2(Bucket=self.bucket)
        objects_in_bucket = []
        try:
            for item in response["Contents"]:
                objects_in_bucket.append(item["Key"])
        except KeyError:
            pass
        return(objects_in_bucket)
    
    def upload_object(self, path: str, key: str) -> None:
        self.client.upload_file(path, self.bucket, key)
    
    def delete_object(self, key: str) -> None:
        self.client.delete_object(Bucket = self.bucket, Key = key)
