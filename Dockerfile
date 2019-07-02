FROM obytes/python:3.4

RUN apk add --update curl \
    git \
    mailcap \
    jpeg-dev \
    zlib-dev \
    libffi-dev \
    openssl-dev \
    imagemagick \
    imagemagick-dev

RUN pip install --upgrade pip

# build-base
COPY requirements.txt /opt/pip/requirements.txt
RUN pip install -r /opt/pip/requirements.txt

ADD . /opt/app
WORKDIR /opt/app
