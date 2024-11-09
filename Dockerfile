FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV GUNICORN_WORKERS=5
ENV GUNICORN_THREADS=2

RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev make ffmpeg

RUN addgroup -S xngroup && adduser -S xnuser -G xngroup

WORKDIR /app

COPY req.txt /app/
RUN pip install --no-cache-dir -r req.txt

RUN mkdir -p /tmp/videos && chmod -R 777 /tmp/videos

COPY . /app

RUN chown -R xnuser:xngroup /app

USER xnuser

EXPOSE 8000

CMD ["sh", "-c", "gunicorn -w ${GUNICORN_WORKERS} -k gevent  --threads ${GUNICORN_THREADS} -b 0.0.0.0:8000 app:app"]
