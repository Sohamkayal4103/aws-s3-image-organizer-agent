import sys
import boto3
from categorize import map_to_category

# Allowed image extensions
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".gif")

def is_image(key: str) -> bool:
    return key.lower().endswith(IMAGE_EXTS)

def list_photos(bucket: str):
    """Yield every object key in the bucket that looks like an image."""
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if is_image(key):
                yield key

def detect_top_label(bucket: str, key: str, max_labels=5, min_conf=80):
    """Return the single top label name from Rekognition."""
    rekog = boto3.client("rekognition")
    resp = rekog.detect_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": key}},
        MaxLabels=max_labels,
        MinConfidence=min_conf,
    )
    labels = resp.get("Labels", [])
    if not labels:
        return "Uncategorized"
    # Labels come sorted by confidence descending
    return labels[0]["Name"].replace(" ", "_")  # replace spaces for folder names

def move_photo(bucket: str, key: str, folder: str):
    """Copy the image into folder/<filename> then delete the original."""
    s3 = boto3.client("s3")
    filename = key.split("/")[-1]
    new_key = f"{folder}/{filename}"
    # Copy
    s3.copy_object(
        Bucket=bucket,
        CopySource={"Bucket": bucket, "Key": key},
        Key=new_key,
    )
    # Delete original
    s3.delete_object(Bucket=bucket, Key=key)
    return new_key

def main():
    if len(sys.argv) != 2:
        print("Usage: python organize_photos.py <your-s3-bucket-name>")
        sys.exit(1)

    bucket = sys.argv[1]
    print(f"Scanning bucket: {bucket}\n")

    for key in list_photos(bucket):
        print(f"Processing: {key}")
        top_label = detect_top_label(bucket, key)
        print(f" -> Detected labels: {top_label}")
        top_label = map_to_category(top_label)

        print(f" -> Top label: {top_label}")
        if not key.startswith(f"{top_label}/"):
            new_key = move_photo(bucket, key, top_label)
            print(f" -> Moved to: {new_key}\n")
        else:
            print(f"Skipping {key} (already in folder {top_label}/)")
        # new_key = move_photo(bucket, key, top_label)
        # print(f" -> Moved to: {new_key}\n")

    print("Done organizing photos!")

if __name__ == "__main__":
    main()
