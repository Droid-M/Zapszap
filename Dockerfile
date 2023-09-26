FROM python:3.9-slim-buster

LABEL maintainer="Marcos Vinícius (droid-M)"

WORKDIR /app

COPY src/ /app

RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py"]