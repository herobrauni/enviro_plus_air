FROM alpine

COPY ./*.sh /usr/src/app/
RUN chmod +x /usr/src/app/*.sh

RUN apk install wget telegraf

# RUN /usr/src/app/download.sh "%%BALENA_ARCH%%"

COPY telegraf.conf /etc/telegraf/telegraf.conf

CMD ["bash","/usr/src/app/entry.sh"]
