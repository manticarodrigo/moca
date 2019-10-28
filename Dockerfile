FROM archlinux/base

RUN mkdir /app
WORKDIR /app

RUN mkdir -p /pacman/cache
COPY os_requirements.txt /app/
RUN xargs -a os_requirements.txt pacman -Syu --needed --cachedir /pacman/cache --force --noconfirm

COPY requirements.txt /app/
COPY requirements /app/requirements
RUN pip install -qqq -r requirements.txt --exists-action i
