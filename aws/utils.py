import sys
import boto3


def upload_to_s3(credentials, region, bucket, to_filename, content, mime_type):
    s3 = boto3.resource(
        's3',
        region_name=region,
        aws_access_key_id=credentials[0],
        aws_secret_access_key=credentials[0])
    s3.Object(bucket, to_filename).put(
        Body=content,
        ACL='public-read',
        ContentType=mime_type)


def download_from_s3(credentials, region, bucket, to_filename, from_filename):
    s3 = boto3.client(
        's3',
        aws_access_key_id=credentials[0],
        aws_secret_access_key=credentials[1],
        region_name=region)
    meta_data = s3.head_object(Bucket=bucket, Key=from_filename)
    total_length = int(meta_data.get('ContentLength', 0))
    downloaded = 0
    def progress(chunk):
        nonlocal downloaded
        downloaded += chunk
        done = int(50 * downloaded / total_length)
        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
        sys.stdout.flush()
    print(f'Downloading {from_filename}')
    with open(to_filename, 'wb') as f:
        s3.download_fileobj(bucket, from_filename, f, Callback=progress)
