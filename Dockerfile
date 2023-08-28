FROM --platform=linux/amd64 python:3.9-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY kittybot.py/ /app

COPY .env/ /app


WORKDIR /app

CMD ["python3", "kittybot.py"]