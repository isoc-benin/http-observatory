FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
    gcc build-essential libpq-dev make \
    && apt-get purge --auto-remove -y git \
	&& rm -rf /var/lib/apt/lists/* \
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --upgrade . && pip install --upgrade -r requirements.txt
