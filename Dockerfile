FROM python:3.7.2-alpine@sha256:2bee696799913a3a2615d469761f355ccee1460e00a22b9e4580cf039a818e24

RUN mkdir -p /app/deploy

COPY deploy/requirements.txt /app/deploy/requirements.txt

RUN python -m venv /venv && \
    PIP_DISABLE_PIP_VERSION_CHECK=true \
    PIP_NO_CACHE_DIR=false \
    /venv/bin/python -m pip install -r /app/deploy/requirements.txt && \
    /venv/bin/python -m pip check

RUN addgroup -g 1000 app \
    && adduser -D -G app -u 1000 app \
    && chown -R app:app /app

USER 1000

WORKDIR /app

ENV DJANGO_LOG_LEVEL WARNING
ENV DJANGO_LOG_REQUESTS 1
ENV DJANGO_LOG_SNS 0
ENV FORWARDED_ALLOW_IPS "*"
ENV GUNICORN_CMD_ARGS "--access-logfile - --timeout 60"
ENV HOST 0.0.0.0
ENV PORT 8000
EXPOSE $PORT
ENV WEB_CONCURRENCY 4
CMD ["/venv/bin/gunicorn", "project.wsgi"]

COPY --chown=app:app . /app

RUN DJANGO_CONFIGURATION=Common DJANGO_SECRET_KEY=dummy /venv/bin/python manage.py collectstatic --noinput
