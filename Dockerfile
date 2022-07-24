FROM python:3.10.5

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app
WORKDIR /app

COPY ./requirements/base.txt /requirements/
RUN pip install --isolated --no-input --compile --exists-action=a -r /requirements/base.txt \
    && rm -rf /requirements/base.txt

# Cron installation
RUN apt-get update && apt-get -y install cron


COPY  ./manage.py /app/manage.py
COPY  ./app /app/app
COPY  ./applift /app/applift
COPY  ./downloader /app/downloader
COPY  ./worker.py /app/worker.py
# for non-production env only
COPY  ./.env /app/.env

EXPOSE 8000
CMD ["gunicorn", "applift.asgi:application", "--bind=0.0.0.0:8000", "--workers=2", "--preload", "--worker-class=uvicorn.workers.UvicornWorker", "--log-level=INFO" ]
