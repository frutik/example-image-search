from fastapi import FastAPI

app = FastAPI()


@app.get("/status")
def status():
    return {"Hello": "World"}
