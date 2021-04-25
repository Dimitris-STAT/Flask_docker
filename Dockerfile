FROM python:3.6
ADD . /app
WORKDIR /app
RUN apt update && apt install -y  
RUN pip3 install -r requirements.txt