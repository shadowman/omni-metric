FROM python:3.9

RUN pip install pipenv

ENV PROJECT_DIR /app

WORKDIR ${PROJECT_DIR}

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/

COPY . ${PROJECT_DIR}/

RUN pipenv install --system --deploy

RUN echo 'PYTHONPATH=${PYTHONPATH}:${PWD}' >> .env
RUN pipenv install
RUN pipenv install --dev

CMD ["pipenv", "run", "python", "omnim/src/cli/app.py"]