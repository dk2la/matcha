FROM debian:buster

# ENV FLASK_ENV=development
ENV FLASK_APP=microblog.py
# ENV FLASK_RUN_HOST=0.0.0.0

# install python
RUN apt -y update && apt -y upgrade
RUN apt-get install -y python3 python3-pip libffi-dev nginx

# install flask
RUN pip3 install flask

WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD nginx -g "daemon off;"
