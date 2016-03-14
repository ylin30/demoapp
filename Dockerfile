# dockerfile
#FROM ylin/ssh_java:openjdk-7
FROM index.alauda.io/ylin30/ubuntu-java-ssh:latest
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

# For logstash
RUN wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
RUN echo "deb http://packages.elastic.co/logstash/2.2/debian stable main" | sudo tee -a /etc/apt/sources.list
RUN sudo apt-get update && sudo apt-get install -y logstash
ADD logstash_files/input.conf /etc/logstash/conf.d
ADD logstash_files/output.conf /etc/logstash/conf.d

ENV ELASTICSEARCH_URL localhost:9200

EXPOSE 8000

CMD ["/opt/tester/default_cmd"]
