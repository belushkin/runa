# pull official base image
FROM python:3.8.1-slim-buster

# create directory for the app user
RUN mkdir -p /usr/src/app

# create the app user
RUN addgroup --system user && adduser --system --no-create-home --group user

# create the appropriate directories
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

# chown all the files to the app user
RUN chown -R user:user /usr/src/app && \
    chmod -R 755 /usr/src/app

RUN chmod +x /usr/src/app/entrypoint.sh

# change to the app user
USER user

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
