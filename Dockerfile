FROM python:3.13-bookworm

WORKDIR /app
COPY requirements.in /app/requirements.in

RUN apt-get update && \
    apt-get install -y libzbar0 && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && pip install pip-tools && \
    pip-compile requirements.in && \
    pip install --no-cache-dir -r requirements.txt && \
    playwright install --with-deps chromium

COPY py_shb_export py_shb_export

ENV SHB_DOCKER=TRUE

# RUN adduser --disabled-password --gecos "" appuser
# USER appuser

CMD ["python", "-m", "py_shb_export"]
