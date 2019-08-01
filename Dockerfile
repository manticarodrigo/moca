FROM archlinux/base

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN mkdir -p /pacman/cache
WORKDIR /app
COPY pacman.conf /etc/pacman.conf
COPY requirements.txt /app/
COPY os_requirements.txt /app/
COPY requirements /app/requirements
COPY apps apps
