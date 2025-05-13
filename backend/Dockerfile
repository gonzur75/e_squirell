FROM python:3.11.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

ARG UID
ARG GID
ARG USER

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install --co-cache-dir pipenv  && pipenv install --system --deploy --ignore-pipfile

COPY . .

EXPOSE 8000

RUN addgroup --gid $GID user
RUN adduser --disabled-password --gecos '' --uid $UID --gid $GID user
USER user


CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
