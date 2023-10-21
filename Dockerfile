FROM apache/airflow:latest-python3.10

COPY pyproject.toml /app/
COPY dist/podcasts_crawler-0.1.0.tar.gz /wheels/


USER root
RUN apt-get update
RUN apt-get -y install git
# change back to base image user
USER 50000

RUN pip install /wheels/podcasts_crawler-0.1.0.tar.gz
