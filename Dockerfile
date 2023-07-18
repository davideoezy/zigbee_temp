FROM alpine:latest
RUN apk add cmd:pip3
COPY requirements.txt /tmp 
WORKDIR /tmp 
ENV TZ=Australia/Melbourne
RUN pip install -r requirements.txt 
WORKDIR /.
ADD zigbee_temp.py /
CMD [ "python", "-u", "./zigbee_temp.py" ]