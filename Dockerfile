FROM python:3.9

# tailing slash is mandatory
ENV TMP_DIR=/tmp/image-service/

RUN mkdir ${TMP_DIR} -p && \
    chmod 0777 ${TMP_DIR} -R

VOLUME [ "${TMP_DIR}" ]

WORKDIR /opt/image-search

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY main.py ./
COPY tasks.py ./
COPY . ./

USER www-data:www-data

CMD ["python", "main.py"]
