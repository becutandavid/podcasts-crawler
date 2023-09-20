FROM python:3.10

WORKDIR /app

COPY pyproject.toml /app/
COPY poetry.lock /app/

ENV VENV_PATH=/poetry_env
RUN python3 -m venv $VENV_PATH
RUN $VENV_PATH/bin/pip install -U pip setuptools
RUN $VENV_PATH/bin/pip install poetry

RUN pip install "apache-airflow[celery]==2.6.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.3/constraints-3.10.txt"

RUN ${VENV_PATH}/bin/poetry config virtualenvs.create false
RUN ${VENV_PATH}/bin/poetry install --only main
