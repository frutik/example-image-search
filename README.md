# example-image-search

Lets try to build (imaginary) images search for the similar images. By writing a simple prototupe step by step.

With blackjack, devops and CI.


## Local

### Install

```
pip install -r requirements.txt
```

### Run

```
uvicorn main:app --reload
```

## Docker

### Configure

```
cp .env.example .env
```

Edit .env providing correct values

### Install

```
docker-compose build
```

### Run

```
docker-compose up
```

## Check code conventions

```
pylint main.py
```