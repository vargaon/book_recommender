FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml ./

RUN pip install poetry==1.7.0 && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-ansi

COPY . ./

CMD poetry run alembic upgrade head && \
    poetry run gunicorn --config gunicorn.conf.py 'src.main:create_app()'