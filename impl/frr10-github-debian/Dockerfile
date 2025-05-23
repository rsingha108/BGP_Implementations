FROM debian:buster
MAINTAINER Rob Gil (rob@rem5.com)

ENV DEBIAN_FRONTEND noninteractive
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn

RUN apt-get update && \
    apt-get install -y libpcre3-dev apt-transport-https ca-certificates curl wget logrotate \
    libc-ares2 libjson-c3 vim procps libreadline7 gnupg2 lsb-release apt-utils \
    libprotobuf-c-dev protobuf-c-compiler tini && rm -rf /var/lib/apt/lists/*

RUN curl -s https://deb.frrouting.org/frr/keys.asc | apt-key add -
RUN echo deb https://deb.frrouting.org/frr $(lsb_release -s -c) frr-stable | tee -a /etc/apt/sources.list.d/frr.list

RUN apt-get update && \
    apt-get install -y frr frr-pythontools && \
    rm -rf /var/lib/apt/lists/*

# Own the config / PID files
RUN mkdir -p /var/run/frr
RUN chown -R frr:frr /etc/frr /var/run/frr

# Simple init manager for reaping processes and forwarding signals
ENTRYPOINT ["/usr/bin/tini", "--"]

# Default CMD starts watchfrr
COPY --chmod=0755 docker-start /usr/lib/frr/docker-start
CMD ["/usr/lib/frr/docker-start"]