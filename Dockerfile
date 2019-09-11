FROM python:3.7-alpine

COPY esp/config.py /esp/
COPY esp/dump.py /esp/
COPY esp/filter_helper.py /esp/
COPY esp/scrape_tweets.py /esp/
COPY esp/stream_listener.py /esp/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /esp
CMD ["python3", "scrape_tweets.py"]