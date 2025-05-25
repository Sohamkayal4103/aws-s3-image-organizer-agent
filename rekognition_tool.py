import boto3

rekog = boto3.client("rekognition")

def detect_labels(bucket: str, key: str, max_labels=5, min_conf=80):
    resp = rekog.detect_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": key}},
        MaxLabels=max_labels, MinConfidence=min_conf
    )
    # return a list of top label names
    return [label["Name"] for label in resp["Labels"]]