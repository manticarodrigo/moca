FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /moca
WORKDIR /moca
COPY requirements.txt /moca/
RUN pip install -r requirements.txt
COPY . /moca
CMD python manage.py runserver 0.0.0.0:$PORT
