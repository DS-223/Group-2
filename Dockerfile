FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR .

COPY requirements.txt .
COPY .env .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR /etl
COPY . .

EXPOSE 3000

CMD ["python", "etl_process.py"]