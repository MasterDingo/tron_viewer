FROM python:3.11.4-slim-buster

WORKDIR /usr/src

# Don't write .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Don't buffer std IO
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install -y git

# Upgrade pip
RUN pip install --upgrade pip
# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt
