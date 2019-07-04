FROM archlinux/base
ENV PYTHONUNBUFFERED 1
RUN mkdir /moca
WORKDIR /moca
COPY requirements.txt /moca/
RUN ["pacman", "-Syu", "--noconfirm"]
RUN ["pacman", "-Su", "--noconfirm", "python", "python-pip", "docker", "docker-compose"]
RUN ["pacman", "-Su", "--noconfirm", "postgresql-libs"]
RUN ["pacman", "-Su", "--noconfirm", "gcc"]
RUN pip install -r requirements.txt
COPY . /moca
