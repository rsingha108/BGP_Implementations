FROM ubuntu:20.04
RUN apt-get update && apt-get -y upgrade 
RUN apt-get install -y lsb-release net-tools wget git vim curl tcpdump iputils-ping tree jq telnet sudo nano gnupg2
RUN curl -s https://deb.frrouting.org/frr/keys.asc | sudo apt-key add -
# possible values for FRRVER: 
# frr-6 frr-7 frr-8 frr-9.0 frr-9.1 frr-10 frr10.0 frr10.1 frr-stable
# frr-stable will be the latest official stable release
ENV FRRVER="frr-8"
RUN echo deb https://deb.frrouting.org/frr $(lsb_release -s -c) $FRRVER | sudo tee -a /etc/apt/sources.list.d/frr.list
RUN apt update && apt install -y frr frr-pythontools
