import csv
import io
import json
import os
import sys

import boto3
import requests

MS1_URL = os.environ["MS1_URL"].rstrip("/")
ADMIN_KEY = os.environ["ADMIN_KEY"]
ANALYTICS_BUCKET = os.environ["ANALYTICS_BUCKET"]

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    aws_session_token=os.environ.get("AWS_SESSION_TOKEN", ""),
    region_name=os.environ["AWS_REGION"],
)

HEADERS = {"X-API-Key": ADMIN_KEY}


def fetch(url):
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def to_csv(records):
    if not records:
        return ""
    buf = io.StringIO()
    fieldnames = list(records[0].keys())
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    for row in records:
        writer.writerow({
            k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v
            for k, v in row.items()
        })
    return buf.getvalue()


def ingest(url, s3_key):
    records = fetch(url)
    body = to_csv(records).encode("utf-8")
    s3.put_object(Bucket=ANALYTICS_BUCKET, Key=s3_key, Body=body, ContentType="text/csv")
    print(f"Subido {s3_key}: {len(records)} registros")


def main():
    ingest(f"{MS1_URL}/api/export/users", "ms1/users/users.csv")
    ingest(f"{MS1_URL}/api/export/zones", "ms1/zones/zones.csv")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
