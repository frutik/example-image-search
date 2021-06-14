import os

from aws.utils import download_from_s3


TMP_PATH=os.getenv('TMP_DIR', '/tmp/')
ANNOY_INDEX = 'test.ann'
ANNOY_INDEX_FULL_PATH = TMP_PATH + ANNOY_INDEX
DOCUMENTS_INDEX = 'id2doc.csv'


def ensure_required(credentials, region, bucket, force=False):
    preload_files = (ANNOY_INDEX, DOCUMENTS_INDEX)
    for f in preload_files:
        if not os.path.isfile(TMP_PATH + f) or force:
            download_from_s3(credentials, region, bucket, TMP_PATH + f, 'annoy/' + f)
