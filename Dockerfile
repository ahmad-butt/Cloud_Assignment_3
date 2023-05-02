FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libc6-dev iputils-ping

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

# EXPOSE 8001

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]