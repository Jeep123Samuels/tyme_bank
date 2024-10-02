# pull official base image
FROM python:3.11.3-slim-buster

RUN apt-get update && \
    apt-get install -y postgresql postgresql-client

WORKDIR /src

RUN ls

COPY . .

RUN pip install -r /src/backend/requirements.txt

WORKDIR /src/backend
EXPOSE 5000
CMD ["flask","run","-h","0.0.0.0"]
