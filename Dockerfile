FROM archlinux/base

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN mkdir -p /pacman/cache
WORKDIR /app
COPY os_requirements.txt /app/
RUN xargs -a os_requirements.txt pacman -Syu --needed --cachedir /pacman/cache --force --noconfirm
COPY requirements.txt /app/
COPY requirements /app/requirements
RUN pip install -qqq -r requirements.txt --exists-action i
COPY apps apps
