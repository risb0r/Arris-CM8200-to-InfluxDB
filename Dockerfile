FROM python:3.5-slim
LABEL maintainer="Tim McBride <tim@deviousgeek.com>"
WORKDIR /app

ADD ["requirements.txt", "cm8200b_stats.py", "./"]
COPY chaperone.conf /etc/chaperone.d/chaperone.conf
RUN pip3 install -r requirements.txt
ENTRYPOINT ["/usr/local/bin/chaperone"]
