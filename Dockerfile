FROM python:2.7

MAINTAINER Mark Anderson <mark@m3b.net>

RUN mkdir -p /usr/src/app/requirements
COPY ./requirements/ /usr/src/app/requirements
COPY ./requirements.txt /usr/src/app/requirements.txt

WORKDIR /usr/src/app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app


RUN ["python", "setup.py", "clean", "-a", "bdist_egg", "-d", "boom"]
RUN chmod +x /usr/src/app/deploy.sh
RUN /usr/src/app/deploy.sh

ENTRYPOINT ["scrapyd"]
