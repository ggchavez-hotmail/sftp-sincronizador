FROM alpine:latest

LABEL maintainer="ggchavez@gmail.com"

ADD . .

RUN apk add --update --no-cache openssh && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config && \
    adduser -h /home/test -s /bin/sh -D test  && \
    echo -n 'test:test' | chpasswd  && \
    chmod +x -v entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]