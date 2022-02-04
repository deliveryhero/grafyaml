FROM python:3.8-slim-bullseye
ADD . /code/
RUN pip3 install tox /code/.
RUN apt-get update && apt-get install -y jq curl
RUN curl -GL# -o /usr/local/bin/yq https://github.com/mikefarah/yq/releases/download/v4.18.1/yq_linux_amd64 \
    && chmod +x /usr/local/bin/yq