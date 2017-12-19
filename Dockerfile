FROM python:3.6-alpine

VOLUME "/root/bowser"
WORKDIR "/root/bowser"
ENTRYPOINT ["pip", "install", "-e", "."]
CMD ["bowser-bot"]
