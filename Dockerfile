FROM python:3.9

WORKDIR /opt/image-search

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY main.py ./

USER www-data:www-data

CMD ["python", "main.py"]
