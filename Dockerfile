FROM python:3.9.6
ENV PYTHONUNBUFFERED 1
WORKDIR /web
COPY requirements.txt /web/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /web/