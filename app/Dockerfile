FROM python:3.7

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./healthcheck.sh

RUN pip install -r requirements.txt
