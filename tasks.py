import os

from invoke import task

from image_search.utils import ensure_required


@task
def ensure_required_files(c, docs=False, bytecode=False, extra=''):
    aws_access_key_id = os.getenv('AWS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_KEY_SECRET')
    aws_region = os.getenv('AWS_REGION')
    aws_s3_bucket = os.getenv('AWS_S3_BUCKET')

    ensure_required(
        (aws_access_key_id, aws_secret_access_key),
        aws_region,
        aws_s3_bucket)

