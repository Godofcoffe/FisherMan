FROM python:3.6-buster

WORKDIR /root

COPY . /root/
RUN cd /root && mkdir output && python3 -m pip install -r requeriments.txt
RUN apt-get update                             \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr           \
 && rm -fr /var/lib/apt/lists/*                \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin \
 && apt-get purge -y ca-certificates curl

ENTRYPOINT ["python", "fisherman.py"]
