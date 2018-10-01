FROM ubuntu:16.04

RUN apt-get update && apt-get install -y nginx git fcgiwrap apache2-utils

RUN service fcgiwrap start

RUN useradd -g www-data git

CMD ["bash", "-c", "service fcgiwrap start && nginx -g 'daemon off;'"]
