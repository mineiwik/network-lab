FROM alpine:3.15

RUN apk --update-cache upgrade

RUN apk add --no-cache openrc

RUN apk add --no-cache openvswitch && \
    rc-update add ovs-modules && \
    rc-update add ovsdb-server && \
    rc-update add ovs-vswitchd

RUN apk add --no-cache tcpdump

RUN apk add --no-cache util-linux

ENTRYPOINT /usr/share/openvswitch/scripts/ovs-ctl start && /bin/sh
