FROM python:3.6-alpine@sha256:e10e26000b4dcfb66c52c11a6a7cc5251f6a95f9512fa9228bb3a66efc6c7075

RUN apk add --no-cache git

COPY requirements.txt /root/
RUN pip install -r /root/requirements.txt

VOLUME "/root/bowser"
WORKDIR "/root/bowser"

ENTRYPOINT ["scripts/entrypoint.sh"]
CMD ["bowser"]
