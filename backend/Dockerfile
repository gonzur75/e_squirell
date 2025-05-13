
FROM python:3.11.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

ARG UID
ARG GID
ARG USER


WORKDIR /app
COPY requirements.txt .

RUN pip install uv && \
    uv pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN addgroup --gid $GID user
RUN adduser --disabled-password --gecos '' --uid $UID --gid $GID user
USER user


CMD python manage.py migrate && uvicorn --host 0.0.0.0 --port 8000 config.asgi:application
