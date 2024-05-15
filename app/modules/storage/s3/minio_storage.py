import uuid
from abc import ABC
import pathlib

from ..system import StorageSystem
from decouple import config
from minio import Minio
from minio.error import S3Error
from urllib.parse import unquote


class MinioS3(StorageSystem, ABC):
    bucket = config('AWS_BUCKET')

    def __init__(self, bucket: str = None):
        self.client = Minio(
            config('AWS_URL'),
            access_key=config('AWS_ACCESS_KEY_ID'),
            secret_key=config('AWS_SECRET_ACCESS_KEY'),
            secure=False
        )

        if bucket:
            self.bucket = bucket

    def read(self, key: str) -> str:
        temp_file = f'/tmp/{uuid.uuid4()}.{pathlib.Path(key).suffix}'
        file_stream = self.client.get_object(self.bucket, unquote(key))
        with open(temp_file, 'wb') as file:
            for d in file_stream.stream(32 * 1024):
                file.write(d)
        return temp_file

    def put(self, key: str):
        pass

    def put_data(self, key: str):
        pass

    def exists(self, key: str) -> bool:
        try:
            object_meta = self.client.stat_object(self.bucket, key)
            return True
        except S3Error:
            return False
