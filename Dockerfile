FROM archlinux/base

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN mkdir -p /pacman/cache
WORKDIR /app
COPY requirements.txt /app/
COPY os_requirements.txt /app/
COPY requirements /app/requirements
COPY apps apps
RUN xargs -a /app/os_requirements.txt pacman -Syu --needed --cachedir /pacman/cache --force --noconfirm
RUN pip install -r /app/requirements.txt --exists-action i
