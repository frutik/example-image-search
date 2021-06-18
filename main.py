import os
import uvicorn

from fastapi import FastAPI, Form
from fastapi.logger import logger

from images import image_by_url

from image_search import SearchIndex
from image_search.utils import ensure_required, ANNOY_INDEX_FULL_PATH


aws_access_key_id = os.getenv('AWS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_KEY_SECRET')
aws_region = os.getenv('AWS_REGION')
aws_s3_bucket = os.getenv('AWS_S3_BUCKET')

app = FastAPI()

search_index = SearchIndex()


@app.on_event("startup")
def startup_event():
    logger.warning('Application startup')
    ensure_required(
        (aws_access_key_id, aws_secret_access_key),
        aws_region,
        aws_s3_bucket)
    search_index.load(ANNOY_INDEX_FULL_PATH)


@app.on_event("shutdown")
def shutdown_event():
    logger.warning('Application shutdown')


@app.get("/status")
def status():
    return {"Hello": "World"}


@app.post("/search_by_url")
async def search_by_url(url: str = Form(...),):
    img = await image_by_url(url)
    return {
        'url': url,
        'data': str(img)
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
