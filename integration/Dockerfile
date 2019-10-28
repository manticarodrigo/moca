FROM archlinux/base

RUN mkdir /app
COPY . app
WORKDIR /app

RUN mkdir -p /pacman/cache
RUN xargs -a os_requirements.txt pacman -Syu --needed --cachedir /pacman/cache --force --noconfirm

RUN pip install -r requirements.txt --exists-action i

ENV PYTHONUNBUFFERED 1
