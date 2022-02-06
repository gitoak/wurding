# FROM node:17

# WORKDIR /app

# # Copy files
# COPY . .

# # Install dependencies
# RUN yarn install --production

# # build backend
# CMD ["nx", "run", "server:build", "--parallel", "--maxParallel=8", "--skip-nx-cache", "--extractLicenses", "--optimization"]

# # build frontend
# CMD ["nx", "run", "web:build",  "--skip-nx-cache", "--extractLicenses", "--optimization", "--outputHashing=all", "--subresourceIntegrity"]



# COPY ./default.conf /etc/nginx/conf.d/default.conf

FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./.flake8 /.flake8
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /server
WORKDIR /server
COPY ./server /server

RUN adduser -D user
USER user