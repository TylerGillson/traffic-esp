FROM python:3.7-alpine

COPY esp/config.py /esp/
COPY esp/tweet_filter.py /esp/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /esp
CMD ["python3", "tweet_filter.py"]