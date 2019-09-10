FROM python:3.7-alpine

COPY esp/config.py /esp/
COPY esp/scrape_tweets.py /esp/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /esp
CMD ["python3", "scrape_tweets.py"]