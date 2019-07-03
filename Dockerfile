FROM python:3.7-alpine3.9

RUN apk --update add --no-cache libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc curl linux-headers \
    python3-dev git bash libressl-dev \
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev gettext

RUN pip install --upgrade pip setuptools wheel

# build-base
COPY requirements.txt /opt/pip/requirements.txt
RUN pip install -r /opt/pip/requirements.txt

ADD . /opt/app
WORKDIR /opt/app
