import os
import uvicorn

from fastapi import FastAPI
from fastapi.logger import logger

from image_search.utils import ensure_required


aws_access_key_id = os.getenv('AWS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_KEY_SECRET')
aws_region = os.getenv('AWS_REGION')
aws_s3_bucket = os.getenv('AWS_S3_BUCKET')

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger.warning('Application startup')
    ensure_required(
        (aws_access_key_id, aws_secret_access_key),
        aws_region,
        aws_s3_bucket)


@app.on_event("shutdown")
def shutdown_event():
    logger.warning('Application shutdown')


@app.get("/status")
def status():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
