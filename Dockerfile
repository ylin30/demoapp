# dockerfile
#FROM ylin/ssh_java:openjdk-7
FROM ylin/ubuntu-java-ssh
MAINTAINER ylin ylin30@gmail.com

RUN sudo apt-get update
RUN sudo apt-get install -y git
RUN sudo apt-get install -y python

ADD files /opt/tester
RUN chmod 700 /opt/tester/default_cmd

RUN mkdir /var/log/tcollector
RUN git clone https://github.com/wangy1931/tcollector
RUN mv tcollector /opt/tester/

ENV CLOUDINSIGHT_SERVER localhost

EXPOSE 8000

CMD ["/opt/tester/default_cmd"]
