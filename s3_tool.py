import boto3
from urllib.parse import urlparse

s3 = boto3.client("s3")

def list_photos(bucket: str, prefix=""):
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [item["Key"] for item in resp.get("Contents", [])]

def move_photo(bucket: str, key: str, target_folder: str):
    copy_src = {"Bucket": bucket, "Key": key}
    new_key = f"{target_folder}/{key.split('/')[-1]}"
    # copy then delete original
    s3.copy_object(Bucket=bucket, CopySource=copy_src, Key=new_key)
    s3.delete_object(Bucket=bucket, Key=key)
    return new_key
