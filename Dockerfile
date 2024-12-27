FROM python:3.10-slim
ENV TZ=Europe/Moscow
WORKDIR /app
COPY . /app
RUN apt-get update \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]