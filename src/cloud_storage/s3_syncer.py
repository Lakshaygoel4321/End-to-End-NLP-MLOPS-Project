import os
import sys
import boto3
from src.logger import logging
from src.exception import USvisaException

class S3Sync:
    def __init__(self):
        try:
            self.s3_resource = boto3.resource("s3")
            self.s3_client = boto3.client("s3")
        except Exception as e:
            raise USvisaException(e, sys)

    def sync_folder_from_s3(self, s3_bucket_url: str, s3_key: str, local_dir: str) -> None:
        """
        Download all files from a specific folder in an S3 bucket to a local directory.
        """
        try:
            bucket = self.s3_resource.Bucket(s3_bucket_url)
            for obj in bucket.objects.filter(Prefix=s3_key):
                target = os.path.join(local_dir, os.path.relpath(obj.key, s3_key))
                os.makedirs(os.path.dirname(target), exist_ok=True)
                if not obj.key.endswith("/"):
                    bucket.download_file(obj.key, target)
                    logging.info(f"Downloaded {obj.key} to {target}")
        except Exception as e:
            raise USvisaException(e, sys)

    def upload_file(self, file_name: str, bucket_name: str, object_name: str = None) -> None:
        """
        Upload a file to S3 bucket.
        """
        try:
            if object_name is None:
                object_name = os.path.basename(file_name)
            self.s3_client.upload_file(file_name, bucket_name, object_name)
            logging.info(f"Uploaded {file_name} to s3://{bucket_name}/{object_name}")
        except Exception as e:
            raise USvisaException(e, sys)

    def download_file(self, bucket_name: str, object_name: str, file_name: str) -> None:
        """
        Download a single file from S3.
        """
        try:
            self.s3_client.download_file(bucket_name, object_name, file_name)
            logging.info(f"Downloaded s3://{bucket_name}/{object_name} to {file_name}")
        except Exception as e:
            raise USvisaException(e, sys)
