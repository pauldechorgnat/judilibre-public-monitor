FROM python:3.10-slim-buster

ADD requirements.txt /

RUN python -m pip install -r /requirements.txt

ADD judilibre-public-monitor /judilibre-public-monitor

WORKDIR /judilibre-public-monitor

EXPOSE 9999

CMD [ "python3", "main.py" ]
