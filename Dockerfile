FROM archlinux/base
ENV PYTHONUNBUFFERED 1
RUN mkdir /moca
WORKDIR /moca
COPY requirements.txt /moca/
RUN ["pacman", "-Syu", "--noconfirm", "python", "python-pip", "docker", "docker-compose", "postgresql-libs", "gcc"]
RUN pip install -r requirements.txt
COPY . /moca
# CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT
