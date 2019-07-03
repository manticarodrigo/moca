FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /moca
WORKDIR /moca
COPY requirements.txt /moca/
RUN pip install -r requirements.txt
RUN apt update -y && apt install -y docker docker-compose
COPY . /moca
