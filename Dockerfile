FROM python:3.13-bookworm

RUN apt-get update && \
    apt-get install -y locales libzbar0 && \
    rm -rf /var/lib/apt/lists/*

RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PYTHONUTF8=1
ENV SHB_DOCKER=TRUE

WORKDIR /app

COPY requirements.in ./
RUN pip install --upgrade pip && \
    pip install pip-tools && \
    pip-compile requirements.in && \
    pip install --no-cache-dir -r requirements.txt && \
    playwright install --with-deps chromium

# Copy in app code last
COPY py_shb_export py_shb_export

CMD ["python", "-m", "py_shb_export"]
