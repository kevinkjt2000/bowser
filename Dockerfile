FROM python:3.6-alpine@sha256:20d014036dc80a73b64d35db756ce5d79abf6e319b545e54719e815d8c9660c5

RUN apk add --no-cache git

COPY requirements.txt /root/
RUN pip install -r /root/requirements.txt

VOLUME "/root/bowser"
WORKDIR "/root/bowser"

ENTRYPOINT ["scripts/entrypoint.sh"]
CMD ["bowser-bot"]
