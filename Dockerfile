FROM archlinux/base
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
COPY requirements /app/requirements
RUN ["pacman", "-Syu", "--noconfirm", "python", "python-pip", "postgresql-libs", "gcc"]
RUN pip install -r requirements.txt
COPY apps apps
CMD python apps/manage.py migrate && python apps/manage.py runserver 0.0.0.0:$PORT
