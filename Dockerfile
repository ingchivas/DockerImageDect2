FROM ubuntu:latest
RUN apt-get update 
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip 
ENV TZ=America/Mexico_City
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y ffmpeg

WORKDIR /motionDetect

ARG EMAIL
ARG EMAILSECRET
ARG SENDEREMAIL

ENV EMAIL=${EMAIL}
ENV EMAILSECRET=${EMAILSECRET}
ENV SENDEREMAIL=${SENDEREMAIL}


COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python3", "-u", "main.py"] 