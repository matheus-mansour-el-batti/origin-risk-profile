FROM python:3.9.1
ENV PYTHONBUFFERED 1

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app

RUN chmod +x /app/run.sh

CMD /app/run.sh
