FROM python:3.9-slim-buster

WORKDIR /app

COPY requeriments.txt requeriments.txt

RUN pip3 install -r requeriments.txt

COPY . .

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
