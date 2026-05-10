FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1



WORKDIR /app


COPY Pipfile Pipfile.lock ./
RUN apk add --no-cache postgresql-client && pip install -U pipenv && pipenv install --system --dev
COPY . .

EXPOSE 8000
ARG UID
ARG GID
ARG USER

CMD python manage.py makemigrations && python manage.py migrate
