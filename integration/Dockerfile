FROM archlinux/base

RUN mkdir /app
WORKDIR /app

# Install pacman packages
COPY os_requirements.txt .
RUN mkdir -p /pacman/cache
RUN xargs -a os_requirements.txt pacman -Syu --needed --cachedir /pacman/cache --noconfirm

# Install python packages
COPY requirements requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --exists-action i

# COPY all application files
COPY . .
