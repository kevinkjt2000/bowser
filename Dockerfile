FROM python:3.6-alpine@sha256:7c3028aa4b9a30a34ce778b1fd4f460c9cdf174515a94641a89ef40c115b51e5

RUN apk add --no-cache git

COPY requirements.txt /root/
RUN pip install -r /root/requirements.txt

VOLUME "/root/bowser"
WORKDIR "/root/bowser"

ENTRYPOINT ["scripts/entrypoint.sh"]
CMD ["bowser-bot"]
