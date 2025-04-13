# src/utils/s3_syncer.py

import os
import sys
import boto3
from src.exception import USvisaException
from src.logger import logging
from botocore.exceptions import NoCredentialsError, ClientError


class S3Sync:
    def __init__(self):
        try:
            self.s3_resource = boto3.resource("s3")
            self.s3_client = boto3.client("s3")
        except Exception as e:
            raise USvisaException(e, sys) from e

    def sync_folder_from_s3(self, bucket_name: str, s3_folder_path: str, local_folder_path: str) -> None:
        """
        Sync a folder from an S3 bucket to a local directory.

        :param bucket_name: Name of the S3 bucket.
        :param s3_folder_path: S3 folder path inside the bucket.
        :param local_folder_path: Local directory to sync files to.
        """
        try:
            logging.info(f"Syncing folder from S3: s3://{bucket_name}/{s3_folder_path} to {local_folder_path}")
            bucket = self.s3_resource.Bucket(bucket_name)

            for obj in bucket.objects.filter(Prefix=s3_folder_path):
                target = os.path.join(local_folder_path, os.path.relpath(obj.key, s3_folder_path))
                os.makedirs(os.path.dirname(target), exist_ok=True)
                bucket.download_file(obj.key, target)
                logging.info(f"Downloaded: {obj.key} to {target}")

        except (NoCredentialsError, ClientError) as e:
            raise USvisaException(f"AWS Credential error or client error: {e}", sys) from e
        except Exception as e:
            raise USvisaException(e, sys) from e

    def upload_file(self, bucket_name: str, local_file_path: str, s3_key: str) -> None:
        """
        Upload a single file to the S3 bucket.

        :param bucket_name: S3 bucket name.
        :param local_file_path: Path to local file.
        :param s3_key: S3 key path to upload the file to.
        """
        try:
            logging.info(f"Uploading {local_file_path} to s3://{bucket_name}/{s3_key}")
            self.s3_client.upload_file(local_file_path, bucket_name, s3_key)
        except Exception as e:
            raise USvisaException(e, sys) from e
