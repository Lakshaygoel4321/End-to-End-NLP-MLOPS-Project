import os
import sys
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from src.logger import logging
from src.exception import USvisaException


class AWSSync:
    def __init__(self):
        try:
            self.s3 = boto3.client('s3')  # Make sure your AWS credentials are set
        except Exception as e:
            raise USvisaException(e, sys) from e

    def sync_folder_from_s3(self, bucket_name: str, s3_folder: str, local_dir: str):
        """
        Downloads all files from a specified S3 folder to a local directory.

        Parameters:
        - bucket_name : str : name of the S3 bucket
        - s3_folder   : str : path in the bucket (can be a "folder"/prefix)
        - local_dir   : str : local directory to download files into
        """
        try:
            logging.info(f"Syncing folder from S3 bucket: {bucket_name}/{s3_folder} -> {local_dir}")

            paginator = self.s3.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket_name, Prefix=s3_folder)

            for page in pages:
                for obj in page.get('Contents', []):
                    s3_file_path = obj['Key']
                    if s3_file_path.endswith('/'):
                        continue  # Skip folders

                    local_file_path = os.path.join(local_dir, os.path.relpath(s3_file_path, s3_folder))
                    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

                    logging.info(f"Downloading {s3_file_path} to {local_file_path}")
                    self.s3.download_file(bucket_name, s3_file_path, local_file_path)

        except NoCredentialsError:
            logging.error("AWS credentials not available")
            raise USvisaException("AWS credentials not available", sys)
        except ClientError as e:
            logging.error(f"Client error during S3 sync: {e}")
            raise USvisaException(e, sys)
        except Exception as e:
            raise USvisaException(e, sys)
