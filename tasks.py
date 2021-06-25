import os
import json

from annoy import AnnoyIndex
from invoke import task
from img2vec_pytorch import Img2Vec
from tqdm.auto import tqdm

from image_search.utils import ensure_required
from aws.utils import download_from_s3, upload_to_s3
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


def build_vector(remote_file):
    try:
        s3i = S3Images(aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key,
                       region_name=aws_region)
        img = s3i.from_s3(aws_s3_bucket, remote_file)
        img2vec = Img2Vec(cuda=False)
        vec = img2vec.get_vec(img, tensor=True)
        return [i[0][0] for i in vec.tolist()[0]]
    except:
        pass

@task
def build_vectors(c, file, help={'file': "File to process. Full path."}):
    DIR = os.path.dirname(file) + '/'
    FILENAME = os.path.basename(file)
    vectors_filename = DIR + FILENAME + '.vec'
    # download_from_s3(
    #     (aws_access_key_id, aws_secret_access_key),
    #     aws_region,
    #     aws_s3_bucket,
    #     TMP_PATH + raw,
    #     'annoy/' + raw)
    raw_data = open(DIR + FILENAME, 'r').readlines()
    vectors_file = open(vectors_filename, 'w')
    for line in tqdm(raw_data, total=len(raw_data)):
        data = json.loads(line)
        if 'vector' not in data:
            vector = build_vector(data['images'].replace('/products/', 'products/'))
            if vector:
                data['vector'] = vector
        vectors_file.write(f'{json.dumps(data)}\n')
        vectors_file.flush()
    vectors_file.close()


def get_idx(path):
    data = open(path, 'r')
    hash = {}
    for f in tqdm(data):
        vvv = f.split(' | ')
        hash[int(vvv[0])] = vvv[1]
    return hash


@task
def build_evaluation(c, evaluation_file, index_file, source_file, help={'file': "File to process. Full path."}):
    annoy = AnnoyIndex(512, 'angular')
    annoy.load(index_file)
    sources = get_idx(source_file)
    evaluation_data = open(evaluation_file, 'r').readlines()
    for line in tqdm(raw_data, total=len(evaluation_data)):
        data = json.loads(line)
        if 'vector' not in data:
            similar = annoy.get_nns_by_vector(data['vector'], 5)
            for s in similar:
                print(sources[s])
