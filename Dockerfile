FROM python:2.7

ARG HTTP_PROXY
ARG HTTPS_PROXY

RUN pip install boto3 Flask

COPY entrypoint.sh /
COPY api.py /

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
