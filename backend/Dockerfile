FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1



WORKDIR /app


COPY Pipfile Pipfile.lock ./
RUN pip install -U pipenv  && pipenv install --system --dev
COPY . .

EXPOSE 8000
ARG UID
ARG GID
ARG USER

CMD python manage.py makemigrations && python manage.py migrate && uvicorn --host 0.0.0.0 --port 8000 config.asgi:application --reload
