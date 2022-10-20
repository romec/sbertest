FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app

ENV FLASK_APP=app.py

CMD python -m flask run --host=0.0.0.0 --port 5000

EXPOSE 5000
