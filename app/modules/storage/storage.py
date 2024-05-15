from decouple import config
from .s3.aws_storage import AwsS3
from .s3.minio_storage import MinioS3


class Storage:

    def __init__(self, bucket: str = None):
        disk = config('FILESYSTEM_DISK')
        if not bucket:
            bucket = config('AWS_BUCKET')

        system = getattr(self, f'create_{disk}_client')
        self.s3 = system(bucket)

    @staticmethod
    def create_s3_client(bucket: str) -> AwsS3:
        return AwsS3(bucket)

    @staticmethod
    def create_minio_client(bucket: str) -> MinioS3:
        return MinioS3(bucket)
