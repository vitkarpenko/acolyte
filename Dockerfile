FROM python:3.7-slim-buster
RUN apt-get update \
    && apt-get upgrade

COPY requirements.txt /app/
WORKDIR /app
RUN pip3 install --upgrade -r requirements.txt
COPY ./app

CMD ["python", "main.py"]
