FROM python:3.11.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

ARG UID
ARG GID
ARG USER

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install --system

COPY . .

EXPOSE 8000

RUN addgroup --gid $GID user
RUN adduser --disabled-password --gecos '' --uid $UID --gid $GID user
USER user


CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
