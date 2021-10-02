FROM ubuntu:latest
MAINTAINER ryanjl9@iastate.edu

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata 
RUN apt install apache2 -y
RUN apt install git -y
RUN apt install cron -y
RUN apt install rsyslog -y
RUN apt install python3.9 -y
RUN apt install python3-pip -y

EXPOSE 20001/tcp
EXPOSE 20002/tcp

COPY requirements.txt ./
COPY startup ./

RUN pip install -U pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /home/sd2021/gitRepo
RUN mkdir -p /var/log/sd2021_server

COPY server.tab /etc/cron.d/server.tab

WORKDIR /home/sd2021/gitRepo
RUN git clone https://github.com/bjpierre/Magic-Sensors-Reimagined.git

RUN chmod 0664 /etc/cron.d/server.tab
RUN touch /var/log/cron.log
RUN crontab /etc/cron.d/server.tab

RUN chmod +x /startup

COPY llp /home/sd2021/
RUN chmod +x /home/sd2021/llp
CMD /home/sd2021/llp
