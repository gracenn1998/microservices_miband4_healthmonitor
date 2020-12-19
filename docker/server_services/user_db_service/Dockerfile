FROM python:3.8-alpine

COPY . /app
WORKDIR /app

RUN \
 apk add --no-cache postgresql-dev gcc python3 musl-dev && \
 pip3 install -r ./user_database/requirements.txt --no-cache-dir

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
