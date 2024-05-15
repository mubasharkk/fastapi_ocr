import uuid
from abc import ABC
import pathlib

from ..system import StorageSystem
from decouple import config
import boto3
import botocore


class AwsS3(StorageSystem, ABC):
    bucket = None

    def __init__(self, bucket: str):
        self.storage = boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            region_name=config('AWS_DEFAULT_REGION')
        )

        if not bucket:
            self.bucket = config('AWS_BUCKET')
        else:
            self.bucket = bucket

    def read(self, key: str) -> str:
        temp_file = f'/tmp/{uuid.uuid4()}.{pathlib.Path(key).suffix}'
        with open(temp_file, 'wb') as f:
            self.storage.download_fileobj(self.bucket, key, f)
        return temp_file

    def put(self, key: str):
        pass

    def put_data(self, data):
        pass

    def exists(self, key: str) -> bool:
        try:
            self.storage.head_object(self.bucket, key)
            return True
        except botocore.exceptions.ClientError as e:
            return False
