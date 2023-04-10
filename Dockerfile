FROM python:3.10-bullseye

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD gunicorn -w 4 -b "0.0.0.0:9000" main:app

EXPOSE 9000