import os
import json

from invoke import task
from img2vec_pytorch import Img2Vec

from image_search.utils import ensure_required
from aws.utils import download_from_s3
from aws.pil_s3 import S3Images


TMP_PATH=os.getenv('TMP_DIR', '/tmp/')

aws_access_key_id = os.getenv('AWS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_KEY_SECRET')
aws_region = os.getenv('AWS_REGION')
aws_s3_bucket = os.getenv('AWS_S3_BUCKET')


@task
def ensure_required_files(c, docs=False, bytecode=False, extra=''):
    ensure_required(
        (aws_access_key_id, aws_secret_access_key),
        aws_region,
        aws_s3_bucket)


@task
def build_vectors(c, docs=False, bytecode=False, extra=''):
    raw = 'images2categories-filtered.json'
    download_from_s3(
        (aws_access_key_id, aws_secret_access_key),
        aws_region,
        aws_s3_bucket,
        TMP_PATH + raw,
        'annoy/' + raw)
    s3i = S3Images(aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key,
                   region_name=aws_region)
    for line in open(TMP_PATH + raw, 'r'):
        data = json.loads(line)
        img = s3i.from_s3(aws_s3_bucket, data['images'].replace('/products/', 'products/'))
        img2vec = Img2Vec(cuda=False)
        vec = img2vec.get_vec(img, tensor=True)
        iv = [i[0][0] for i in vec.tolist()[0]]
        print(iv)
