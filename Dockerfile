FROM python:3.6-alpine3.7 AS base
COPY requirements.txt /
WORKDIR /
RUN apk add --no-cache && pip install --upgrade pip &&  pip install --no-cache-dir -r requirements.txt

FROM base
COPY ./ /SC_Alertbot
WORKDIR /SC_Alertbot
ENTRYPOINT ["python","bot_listener.py"]