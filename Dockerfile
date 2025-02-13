FROM python:3.13-slim

RUN apt-get update && apt-get install -y wget libnss3 libx11-xcb1 libxcomposite1 libxrandr2 libxi6 libxcursor1 \
    libxdamage1 libxext6 libxfixes3 libxrender1 libasound2 libpangocairo-1.0-0 libpango-1.0-0 libcairo2 \
    libxshmfence1 libdbus-glib-1-2 libxt6 libgtk-3-0 libgdk-pixbuf2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install pip-tools && pip-sync requirements.txt

RUN playwright install --with-deps

COPY . .

RUN touch /.container_marker

CMD ["python", "-m", "scraper", "--container"]
