
FROM python:3.8.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api

COPY . .


RUN apk update && \
    apk add --no-cache build-base python3-dev postgresql-dev
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh


EXPOSE 8000

ENTRYPOINT [ "sh","entrypoint.sh" ]

