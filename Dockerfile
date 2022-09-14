FROM python:3.9.7

RUN mkdir /disk_service
COPY . /disk_service/
WORKDIR /disk_service

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
RUN pip3 install mysqlclient

CMD ["python", "./drf/manage.py", "runserver", "0.0.0.0:80"]
