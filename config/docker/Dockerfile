FROM python:3.9

COPY . ./app

WORKDIR /app

ARG API_KEY

RUN pip install -r requirements.txt

RUN sed -i "s/API_KEY/${API_KEY}/g" templates/Game.html

ENTRYPOINT python server.py