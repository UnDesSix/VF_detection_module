FROM ubuntu:latest

RUN mkdir /app

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
	apt-get install -y libpq-dev python3-dev unixodbc-dev && \
	apt-get install -y vim cron && \
	apt-get install -y python3.9 python3-pip

ADD config/requirements.txt /app

WORKDIR /app

RUN pip install --no-cache-dir -r config/requirements.txt
RUN /usr/bin/crontab config/crontab.txt

RUN	ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime && \
	dpkg-reconfigure -f noninteractive tzdata

RUN mkdir -p /root/transfers_tools/csv /root/detection_tools/list/ /root/detection_tools/csv/
RUN touch /root/detection_tools/file.log

ADD src /app

ADD init_db.sh /app
ADD update_db.sh /app

CMD ["cron", "-f"]