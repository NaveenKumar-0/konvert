import os
import uuid
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load env explicitly
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")

if not AWS_S3_BUCKET:
    raise RuntimeError("AWS_S3_BUCKET is not set")

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

def upload_file(file_bytes: bytes, filename: str, content_type: str, folder: str) -> str:
    ext = Path(filename).suffix
    s3_key = f"{folder}/{uuid.uuid4()}{ext}"

    s3_client.put_object(
        Bucket=AWS_S3_BUCKET,
        Key=s3_key,
        Body=file_bytes,
        ContentType=content_type,
    )

    return s3_key


def generate_download_url(s3_key: str, expires_in: int = 3600) -> str:
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": AWS_S3_BUCKET,
                "Key": s3_key,
            },
            ExpiresIn=expires_in,
        )
    except ClientError:
        return None
