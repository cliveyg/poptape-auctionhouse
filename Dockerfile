FROM python:3.7-alpine

# add bash etc as alpine version doesn't have these
#RUN apk add --no-cache bash git gawk sed grep bc coreutils 

# these modules enable us to build bcrypt
#RUN apk --no-cache add --virtual build-dependencies gcc g++ make libffi-dev openssl-dev

# install openssl 
#RUN  apk update \
#  && apk add openssl \
#  && rm -rf /var/cache/apk/*

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
#RUN apk update && apk add postgresql-dev
# add bash etc as alpine version doesn't have these
RUN apk add linux-headers
RUN apk add --no-cache bash gawk sed grep bc coreutils
RUN apk --no-cache add libpq

# this needs to match the directory/package name of the python app
# TODO: Copy only specific needed files and folders across
COPY . /auctionhouse
WORKDIR /auctionhouse

RUN rm .coverage
RUN rm -r .git/
RUN rm -r auction/tests
RUN rm -r auctionhouse/tests
RUN mkdir -p /auctionhouse/log

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Define environment variables here
# args are passed it from cli or docker-compose.yml
#ARG poptape_auth_user
#ARG poptape_auth_pass
#ENV NAME cliveyg
#ENV POPTAPE_AUTH_USER {$poptape_auth_user}
#ENV POPTAPE_AUTH_PASS {$poptape_auth_pass}

# if -u flag in CMD below doesn't work 
# then uncomment this to see python
# print statements in docker logs
ENV PYTHONUNBUFFERED=0

# run gunicorn
#CMD ["gunicorn", "-b", "0.0.0.0:9100", "auctionhouse.wsgi:application"]
#CMD ["python", "manage.py", "process_tasks"]

# Run start script for background tasks
CMD ["./run_app.sh"]
#RUN ["python", "manage.py", "process_tasks"]

# Make port 9100 available to the world outside this container
EXPOSE 9100
