FROM alpine:3.15

RUN apk --update-cache upgrade

RUN apk add --no-cache openrc

RUN apk add --no-cache nano

RUN apk add --no-cache tcpdump

RUN apk add --no-cache util-linux

RUN mkdir -p /run/openrc && touch /run/openrc/softlevel

COPY ./interfaces /etc/network/interfaces

RUN rc-update add networking

ENTRYPOINT openrc && rc-service networking start & /bin/sh