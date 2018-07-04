FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /flask-deployment
WORKDIR /flask-deployment
RUN conda env create --file environment.yml
ENTRYPOINT ["python"]
CMD ["run_keras_server.py"]

