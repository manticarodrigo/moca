FROM 'python'
RUN pip install django
VOLUME /moca
WORKDIR /moca
EXPOSE 8000
ENTRYPOINT ./manage.py runserver 0.0.0.0:8000
