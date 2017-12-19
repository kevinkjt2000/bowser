FROM python:3.6-alpine

WORKDIR "/root"
COPY bowser /root/bowser
COPY scripts /root/scripts
COPY setup.py /root/setup.py
RUN pip install -e .

ENTRYPOINT ["bowser-bot"]
