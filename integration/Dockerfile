FROM archlinux/base

RUN mkdir /app
WORKDIR /app

# Install pacman packages
COPY os_requirements.txt /app
RUN mkdir -p /pacman/cache
RUN xargs -a os_requirements.txt pacman -Syu --needed --cachedir /pacman/cache --force --noconfirm

# Install python packages
COPY requirements /app
COPY requirements.txt /app
RUN pip install -r requirements.txt --exists-action i

# COPY all application files
COPY . app
